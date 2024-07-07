from django.db import models
from django.conf import settings

class CoinPackage(models.Model):
    name = models.CharField(max_length=100)
    coins = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coin_package = models.ForeignKey(CoinPackage, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.coin_package.name}"
