# Generated by Django 5.0.6 on 2024-12-22 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BidPlacement', '0004_alter_bid_bid_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='ai_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
