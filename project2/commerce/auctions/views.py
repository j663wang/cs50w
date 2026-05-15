from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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

@login_required
def new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        
        if Listing.objects.filter(title=title).first() is not None:
            return render(request, "auctions/error.html", {
                "message": "Listing with this title already exists."
            })

        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            owner=request.user
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html")
    
def listing_view(request, list_id):
    listing = Listing.objects.get(pk=list_id)
    comments = listing.comments.all().order_by("-timestamp")
    if request.user.is_authenticated:
        in_wishlist = request.user.wishlist.filter(pk=listing.id).exists()
    else:        
        in_wishlist = False
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "in_wishlist": in_wishlist
    })

@login_required
def wishlist(request):
    user = request.user
    wishlist_items = user.wishlist.all()
    return render(request, "auctions/wishlist.html", {
        "wishlist_items": wishlist_items
    })

@login_required
def place_bid(request, list_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=list_id)
        bid_amount = request.POST["bid_amount"]
        current_high = listing.current_high if listing.current_high is not None else listing.starting_bid

        if float(bid_amount) <= float(current_high):
            return render(request, "auctions/error.html", {
                "message": "Bid must be no less than the current bid."
            })

        bid = Bid(
            listing=listing,
            bidder=request.user,
            amount=bid_amount
        )
        bid.save()

        listing.current_high = bid_amount
        listing.save()

        return HttpResponseRedirect(reverse("listing_view", args=[list_id]))

@login_required
def close_listing(request, list_id):
    listing = Listing.objects.get(pk=list_id)
    listing.active = False
    highest_bidder = listing.bids.order_by("-amount","-timestamp").first().bidder

    if highest_bidder is not None:
        listing.winner = highest_bidder

    listing.save()

    return HttpResponseRedirect(reverse("listing_view", args=[list_id]))

@login_required
def add_comment(request, list_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=list_id)
        content = request.POST["comment_content"]

        comment = Comment(
            listing=listing,
            commenter=request.user,
            content=content
        )
        comment.save()

        return HttpResponseRedirect(reverse("listing_view", args=[list_id]))

@login_required
def toggle_wishlist(request, list_id):
    listing = Listing.objects.get(pk=list_id)
    user = request.user

    if user.wishlist.filter(pk=listing.id).exists():
        user.wishlist.remove(listing)
    else:
        user.wishlist.add(listing)

    return HttpResponseRedirect(reverse("listing_view", args=[list_id]))