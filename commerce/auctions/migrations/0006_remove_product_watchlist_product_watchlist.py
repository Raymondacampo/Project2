# Generated by Django 4.2.6 on 2023-11-17 02:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_product_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='product',
            name='watchlist',
            field=models.ManyToManyField(null=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
