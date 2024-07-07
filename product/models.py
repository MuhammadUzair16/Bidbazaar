from django.db import models

class Product (models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.CharField(max_length=200,unique=True)
    description = models.CharField(max_length=200, unique=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name