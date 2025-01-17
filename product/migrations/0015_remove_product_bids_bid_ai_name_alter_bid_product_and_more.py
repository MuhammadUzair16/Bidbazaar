# Generated by Django 5.0.6 on 2024-12-21 15:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_product_bids_alter_bid_product'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='bids',
        ),
        migrations.AddField(
            model_name='bid',
            name='ai_name',
            field=models.CharField(blank=True, help_text='Name of the AI bot placing the bid.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BidPlacement', to='product.product'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_bids', to=settings.AUTH_USER_MODEL),
        ),
    ]
