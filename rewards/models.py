from django.db import models
from django.conf import settings  # For using the custom user model
from BidPlacement.models import Product, Bid


class RewardPool(models.Model):

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reward Pool - {self.total_amount} coins"


class UserRewardPoints(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"


class RewardTransaction(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=[('distribution', 'Distribution'), ('redemption', 'Redemption')])
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} points - {self.transaction_type} for {self.product.name if self.product else 'N/A'}"
