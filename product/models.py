from django.db import models
from accounts.models import Account
from django.conf import settings
from django.utils.timezone import now

# In product/models.py
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    auction_end_time = models.DateTimeField(default=now)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_products",
        help_text="The user who won the auction for this product."
    )

    def __str__(self):
        return self.product_name



class Bid(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='product_bids')
    product = models.ForeignKey(Product, related_name='bids', on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.bid_amount}"