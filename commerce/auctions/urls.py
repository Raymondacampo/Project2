from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.view_watchlist, name="view_watchlist"),
    path("<int:item_id>", views.item, name="item"),
    path("<int:item_id>/bid", views.bid, name="bid"),
    path("<int:item_id>/watchlist", views.add_watchlist, name="watchlist"),
    path("<int:item_id>/close", views.close, name="close"),
    path("<int:item_id>/comment", views.comment, name="comment")
    
]
