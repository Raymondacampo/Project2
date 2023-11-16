from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Bid, Comment, Product

class CreateProduct(forms.Form):
    name = forms.CharField(max_length=50, min_length=5)
    description = forms.CharField(max_length=300)
    price = forms.IntegerField(min_value=0)
    image = forms.URLField()

def index(request):
    items = Product.objects.all()
    return render(request, "auctions/index.html", {
        "items":items
    })


def create(request):
    user = request.user
    if request.method == 'POST':
        Item_name = request.POST['name']
        Item_description = request.POST['description']
        Item_price = request.POST['price']
        Item_image = request.POST['image']
        Product.objects.create(owner = user, name = Item_name, description = Item_description, price = Item_price, image = Item_image)
    
    form = CreateProduct()
    return render(request, "auctions/create.html", {
        "form":form
    })








def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
