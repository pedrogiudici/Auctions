from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'userib')
    bid = models.IntegerField()
    winner = models.BooleanField(default=False)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useric')
    comment = models.CharField(max_length=150)

class AuctionListing(models.Model):
    title = models.CharField(max_length=16)
    description = models.CharField(max_length=150)
    startbid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='bidia')
    url = models.URLField(blank=True)
    category = models.CharField(max_length=16, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'useria')
    comment = models.ManyToManyField(Comment, related_name= 'commentia', blank=True) 
    def __str__(self):
        return f'{self.title}'


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useriw')
    auction = models.ManyToManyField(AuctionListing, blank=True, related_name='auctioniw')
