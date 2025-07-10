from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Brand(models.Model):
    brandName = models.CharField(max_length=50)

    def __str__(self):
        return self.brandName

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

    def __str__(self):
        return str(self.bid)

class Listings(models.Model):
    title = models.CharField(max_length=30)
    discription = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, related_name="brand")
    watchlist = models.ManyToManyField(User, blank=True, related_name="listingWatchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comments on {self.listing}"


