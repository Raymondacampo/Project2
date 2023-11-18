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

class Categorie(models.Model):
    categorie = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.categorie}"

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="products")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    active = models.BooleanField(default=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images', null=True)
    winner = models.ForeignKey(Bid, on_delete=models.SET_NULL, null=True, blank=True, related_name="product")
    comments = models.ManyToManyField(Comment, blank=True, related_name="product")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name="product")

    def __str__(self):
        return f"{self.id} {self.name}"
