from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.new_listing, name="new_listing"),
    path("listing/<int:list_id>", views.listing_view, name="listing_view"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("place_bid/<int:list_id>", views.place_bid, name="place_bid"),
    path("close_listing/<int:list_id>", views.close_listing, name="close_listing"),
    path("add_comment/<int:list_id>", views.add_comment, name="add_comment"),
    path("modify_wishlist/<int:list_id>", views.toggle_wishlist, name="modify_wishlist"),
]
