from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Bid, Comment, Product, Categorie
from django.contrib.auth.decorators import login_required

class CreateProduct(forms.Form):
    name = forms.CharField(max_length=50, min_length=5)
    description = forms.CharField(max_length=300)
    price = forms.IntegerField(min_value=0)
    image = forms.URLField()

class Comment_form(forms.Form):
    comment = forms.CharField(max_length=300)

def index(request):
    items = Product.objects.all()

    return render(request, "auctions/index.html", {
        "items":items
    })


@login_required
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


def item(request, item_id):
    form = Comment_form()
    item = Product.objects.get(pk=item_id)
    user = request.user
    comments = item.comments.all()
    if item.winner != None:
        bid = Bid.objects.get(pk=item.winner.id)
        value = bid.bidamount + 1
    else:
        bid = "No bets yet"
        value = item.price
        if item.owner != user:
            return render(request, "auctions/item.html", {
                "item":item,
                "form":form,
                "bid":bid,
                "value":value,
                "coments":comments
            })
        else:
            return render(request, "auctions/myitem.html", {
                "item":item,
                "form":form,
                "bid":bid,
                "value":value,
                "coments":comments
            })

@login_required
def add_watchlist(request, item_id):
    user = request.user
    product = Product.objects.get(pk=item_id)
    product.watchlist.add(user)
    return render(request, "auctions/watchlist.html")

def view_watchlist(request):
    user = request.user
    u = User.objects.get(pk=user.id)
    items = u.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "items": items
    })

@login_required
def bid(request, item_id):
    user = request.user
    if request.method == 'POST':
        item = Product.objects.get(pk=item_id)
        amount = request.POST['amount']
        apuesta = Bid.objects.create(user = user, bidamount = amount)
        apuesta.save()
        item.winner = apuesta
        item.save()
        return HttpResponseRedirect(reverse('index'))


def close(request, item_id):
    item = Product.objects.get(pk=item_id)  
    item.active = False
    item.save()
    return HttpResponseRedirect(reverse('item', args=[item_id]))


def comment(request, item_id):
    if request.method == 'POST':
        c = request.POST['comment']
        item = Product.objects.get(pk=item_id)
        comment = Comment.objects.create(user = request.user, comment = c)
        comment.save()
        item.comments.add(comment)
        return HttpResponseRedirect(reverse('item', args=[item_id]))


def categories(request):
    categories = Categorie.objects.all()
    return render(request, "auctions/categories.html", {
        "categories":categories
    })

def category_items(request, categorie_id):
    cat = Categorie.objects.get(pk=categorie_id)
    items = cat.product.all()
    return render(request, "auctions/itemcategories.html", {
        "categories":items
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
