# Generated by Django 5.0.6 on 2024-10-27 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_bid_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_available',
        ),
        migrations.AddField(
            model_name='product',
            name='unavailable_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
