from django.contrib import admin
from .models import User, Bid, Comment, Product, Categorie
# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(Categorie)