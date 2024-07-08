# Generated by Django 5.0.6 on 2024-07-07 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_is_superadmin_account_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='coin_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
