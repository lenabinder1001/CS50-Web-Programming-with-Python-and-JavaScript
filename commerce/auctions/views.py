from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def all_listings(request):
    return render(request, "auctions/all_listings.html", {
        "listings": Listing.objects.all()
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

def create(request):
    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })

def create_listing(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        if request.POST["image"]:
            image = request.POST["image"]
        if request.POST["category"]:
            category = Category.objects.get(pk=request.POST["category"])
        listing = Listing.objects.create(title=title,
                                description=description,
                                firstBid=bid,
                                image=image,
                                category=category,
                                creator=user)
        listing.save()
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all()
        })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    try:
        watchlist = Watchlist.objects.get(user=request.user)
    except:
        watchlist = ""
    comments = listing.comments.all()
    if listing.lastBid:
        min_value = float(listing.lastBid.value) + 0.01
    else:
        min_value = float(listing.firstBid) + 0.01
    return render(request, 'auctions/listing.html', {'listing': listing, 'watchlist': watchlist, 'min_value': min_value, 'comments': comments})

def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {'categories': categories})

def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category_id)
    return render(request, 'auctions/category_detail.html', {'listings': listings, 'category': category})

def watchlist(request, user_id):
    try:
        watchlist = Watchlist.objects.get(user=user_id)
        return render(request, 'auctions/watchlist.html', {'watchlist': watchlist})
    except Watchlist.DoesNotExist:
        return render(request, 'auctions/watchlist.html', {'not_working': True})

def watchlist_add(request, user_id, listing_id):
        watchlist = Watchlist.objects.get(user=user_id)
        listing = Listing.objects.get(pk=listing_id)
        comments = listing.comments.all()
        watchlist.listings.add(listing)
        watchlist.save()
        if listing.lastBid:
            min_value = float(listing.lastBid.value) + 0.01
        else:
            min_value = float(listing.firstBid) + 0.01
        return render(request, 'auctions/listing.html', {'listing': listing, 'watchlist': watchlist, 'min_value': min_value, 'comments': comments})

def watchlist_remove(request, user_id, listing_id):
    watchlist = Watchlist.objects.get(user=user_id)
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all()
    watchlist.listings.remove(listing)
    watchlist.save()
    if listing.lastBid:
        min_value = float(listing.lastBid.value) + 0.01
    else:
        min_value = float(listing.firstBid) + 0.01
    return render(request, 'auctions/listing.html', {'listing': listing, 'watchlist': watchlist, 'min_value': min_value, 'comments': comments})

def bid(request, listing_id, user_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=user_id)
    comments = listing.comments.all()
    if request.method == "POST":
        bid_value = request.POST["bid"]
    bid = Bid.objects.create(listing=listing,
                                            user=user,
                                            value=bid_value)
    bid.save()
    listing.lastBid = bid
    listing.save()
    if listing.lastBid:
        min_value = float(listing.lastBid.value) + 0.01
    else:
        min_value = float(listing.firstBid) + 0.01
    return render(request, 'auctions/listing.html', {'listing': listing, 'watchlist': watchlist, 'min_value': min_value, 'comments': comments})

def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all()
    listing.active = False
    listing.save()
    watchlist = Watchlist.objects.get(user=request.user)
    if listing.lastBid:
        min_value = float(listing.lastBid.value) + 0.01
    else:
        min_value = float(listing.firstBid) + 0.01
    return render(request, 'auctions/listing.html', {'listing': listing, 'watchlist': watchlist, 'min_value': min_value, 'comments': comments})

def comment(request, listing_id, user_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=user_id)
    comments = listing.comments.all()
    if request.method == "POST":
        comment_text = request.POST["comment"]
        comment = Comment.objects.create(listing=listing,
                                        text=comment_text,
                                            user=user,)
        comment.save()
    if listing.lastBid:
        min_value = float(listing.lastBid.value) + 0.01
    else:
        min_value = float(listing.firstBid) + 0.01
    return render(request, 'auctions/listing.html', {'listing': listing, 'watchlist': watchlist, 'min_value': min_value, 'comments': comments})
    

