# Generated by Django 5.0.6 on 2024-10-27 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_remove_product_is_available_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='unavailable_until',
        ),
        migrations.AddField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
