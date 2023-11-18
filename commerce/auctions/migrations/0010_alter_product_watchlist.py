# Generated by Django 4.2.6 on 2023-11-17 02:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_product_watchlist_alter_product_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]