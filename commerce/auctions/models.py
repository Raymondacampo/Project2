from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="bids")
    bidamount = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="comments")
    comment = models.CharField(max_length=300)

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="products")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    active = models.BooleanField(default=True)
    price = models.IntegerField(default=0)
    winner = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, related_name="product")
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name="product")