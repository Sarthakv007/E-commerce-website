from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Brand, Listings, Comment, Bid


def index(request):
    activeListings = Listings.objects.filter(isActive = True)
    allBrands = Brand.objects.all()
    return render(request, "auctions/index.html", {
        "Listing" : activeListings,
        "brands" : allBrands
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

def createListing(request) :
    if request.method == "GET" :
        allBrands = Brand.objects.all()
        return render(request, "auctions/create.html", {
            "brands":allBrands
        })
    else :
        title=request.POST["title"]
        discription=request.POST["discription"]
        price=request.POST["price"]
        imageurl=request.POST["imageurl"]
        brand=request.POST["brand"]
        curruntUser=request.user

        brandData = Brand.objects.get(brandName = brand)
        bid = Bid( bid=float(price), user = curruntUser)
        bid.save()
        newListing = Listings(
            title = title,
            discription = discription,
            price = bid,
            image_url = imageurl,
            brand = brandData,
            owner = curruntUser
        )

        newListing.save()
        return HttpResponseRedirect(reverse(index))

def displayBrands(request) :
    if request.method == "POST":
        brandFromForm = request.POST['brand']
        brand_name = Brand.objects.get( brandName = brandFromForm)
        activeListings = Listings.objects.filter(isActive = True, brand=brand_name)
        allBrands = Brand.objects.all()
        return render(request, "auctions/index.html", {
            "Listing" : activeListings,
            "brands" : allBrands
        })

def listing(request, id) :
    listingData = Listings.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html",{
        "listing" : listingData,
        "isListingInWatchlist" : isListingInWatchlist,
        "allComments" : allComments,
        "isOwner" : isOwner
    })

def closeAuction(request, id):
    listingData = Listings.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isListingInWatchlist = request.user in listingData.watchlist.all()
    isOwner = request.user.username == listingData.owner.username
    allComments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html",{
        "listing" : listingData,
        "isListingInWatchlist" : isListingInWatchlist,
        "allComments" : allComments,
        "isOwner" : isOwner,
        "message" : "Congratulations! Auction is closed."
    })

def removeWatchlist(request, id):
    listingData = Listings.objects.get(pk=id)
    curruntUser = request.user
    listingData.watchlist.remove(curruntUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchlist(request, id):
    listingData = Listings.objects.get(pk=id)
    curruntUser = request.user
    listingData.watchlist.add(curruntUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def displayWatchlist(request) :
    curruntUser = request.user
    listings = curruntUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "Listing" : listings
    })

def addComment(request, id):
    curruntUser = request.user
    listingData = Listings.objects.get(pk=id)
    message = request.POST.get('comment', '').strip()
    if not message:
        # Handle the case where the comment is missing
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    newComment = Comment(
        author = curruntUser,
        listing = listingData,
        message = message
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addBid(request, id) :
    newBid = int(request.POST.get('newBid', 0))
    listingData = Listings.objects.get(pk=id)
    isOwner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    if newBid > listingData.price.bid :
        updateBid = Bid(user=request.user, bid=newBid)
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html",{
            "listing":listingData,
            "message":"Bid updated successfully",
            "update" : True,
            "isListingInWatchlist" : isListingInWatchlist,
            "allComments" : allComments,
            "isOwner" : isOwner
        })
    else:
        return render(request, "auctions/listing.html",{
            "listing":listingData,
            "message":"Bid update failed",
            "update" : False,
            "isListingInWatchlist" : isListingInWatchlist,
            "allComments" : allComments,
            "isOwner" : isOwner
        })

