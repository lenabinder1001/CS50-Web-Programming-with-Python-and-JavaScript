from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    image = models.CharField(default=0, max_length=300)
    bids = models.ManyToManyField('Bid', related_name='auctionBids', blank=True)
    firstBid = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    lastBid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='lastBid', blank=True, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='relatedCategory', blank=True, null=True)
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name="listingCreator", blank=True, null=True)

    def __str__(self):
        return f"{self.title}: {self.description}"

class Bid(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="auctionBids")
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="bidUser", blank=True, null=True)
    value = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return f"{self.listing}: {self.value}$"

class Comment(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=300)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="commentUser", blank=True, null=True)

    def __str__(self):
        return f"{self.listing}: {self.text}"

class Category(models.Model):
    title = models.CharField(default=0, max_length=60)

    def __str__(self):
        return f"{self.title}"

class Watchlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_watchlist")
    listings = models.ManyToManyField('Listing', related_name="listings_watchlist", blank=True)

    def __str__(self):
        return f"{self.user}, {self.listings} "