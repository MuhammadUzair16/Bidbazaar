# Generated by Django 5.0.6 on 2025-01-08 08:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_remove_product_is_auction_ended_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='winner',
            field=models.ForeignKey(blank=True, help_text='The user who won the auction for this product.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_products', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
