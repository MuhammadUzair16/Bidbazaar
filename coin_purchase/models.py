from django.db import models
from django.conf import settings

class CoinPackage(models.Model):
    name = models.CharField(max_length=100)
    coins = models.IntegerField()
    coin_price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    coin_package = models.ForeignKey(CoinPackage, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coin_purchases')
    purchase_date = models.DateTimeField(auto_now_add=True)
    coins = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.coin_package.name}"

