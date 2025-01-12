from django.db import models
from django.conf import settings
from product.models import Product
from django.db.models import Sum

class Bid(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='bidplacement_bids',
        on_delete=models.CASCADE
    )
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    ai_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.ai_name:
            return f"AI Bot {self.ai_name} placed a bid on {self.product} for {self.bid_amount} coins"
        elif self.user:
            return f"Bid by {self.user} on {self.product} for {self.bid_amount} coins"
        return "Unknown bid"

    def save(self, *args, **kwargs):
        if self.bid_amount <= 0:
            raise ValueError("Bid amount must be greater than zero.")

        if self.ai_name:
            self.user = None

            total_user_bids = self.product.bidplacement_bids.filter(ai_name__isnull=True).aggregate(total_bid=Sum('bid_amount'))['total_bid'] or 0
            if total_user_bids >= self.product.price:
                return

        if self.user:
            last_bid = self.product.bidplacement_bids.order_by('-bid_time').first()
            if last_bid and last_bid.bid_amount == self.bid_amount and last_bid.user == self.user:
                raise ValueError("Duplicate bid detected. Do not bid the same amount as your previous bid.")

            profile = getattr(self.user, 'profile', None)
            if not profile:
                raise ValueError("User profile does not exist.")
            if profile.coins >= self.bid_amount:
                profile.coins -= self.bid_amount
                profile.save()
            else:
                raise ValueError("Insufficient coins to place a bid.")

        # Save the bid
        super().save(*args, **kwargs)
