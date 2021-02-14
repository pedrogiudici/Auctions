from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import AuctionListing, User, Watchlist, Bid, Comment
from django.contrib.auth.decorators import login_required

def index(request):
    auc = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        'auc': auc
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
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        try:
            AuctionListing.objects.get(title=title)
            return render(request, 'auctions/create.html', {
                'message': 'This title already exists'
            })
        except:
            description = request.POST['description']
            startbid = request.POST['startbid']
            urlimage = request.POST['urlimage']
            category = request.POST['category'].replace('/', '-')
            user = User.objects.get(username=request.POST['user'])
            startbid = Bid(user=user, bid= startbid)
            startbid.save()
            AuctionListing(title= title, description= description, startbid= startbid, url= urlimage, category= category, user= user).save()
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/create.html')

def auction(request, auction_id):
    a = AuctionListing.objects.get(id=auction_id)
    winner = None
    if a.startbid.winner == True:
        winner = a.startbid.user
    return render(request, 'auctions/auction.html',{
        'id': a.id,
        'title': a.title,
        'description': a.description,
        'startbid': a.startbid.bid,
        'urlimage': a.url,
        'category': a.category,
        'usern': a.user,
        'winner': winner,
        'comment': a.comment.all()
    })
    
@login_required
def addwatchlist(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['user'])
        auction = AuctionListing.objects.get(title=request.POST['auction'])
        try:
            auction.auctioniw.get(user= user).delete()
            return HttpResponseRedirect(reverse('auction', args=(auction.id,)))
        except:
            try:
                a = Watchlist.objects.get(user=user)
                a.auction.add(auction)
            except:
                Watchlist.objects.create(user=user)
                a = Watchlist.objects.get(user=user)
                a.auction.add(auction)
            return HttpResponseRedirect(reverse('auction', args=(auction.id,)))
@login_required
def watchlist(request, user_username):
    user = User.objects.get(username=user_username)
    try:
        a = Watchlist.objects.get(user=user)
    except:
        return render(request, 'auctions/watchlist.html')
    return render(request, 'auctions/watchlist.html', {
        'watchlist': a.auction.all()
    })
@login_required
def bid(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['user'])
        auction = AuctionListing.objects.get(title=request.POST['auction'])
        bid = request.POST['bid']
        try:
            a = Bid.objects.get(user=user)
            a.bid = bid
            a.save()
        except:
            a = Bid(user=user, bid=bid)
            a.save()
        auction.startbid = a
        auction.save()
        return HttpResponseRedirect(reverse('auction', args=(auction.id,)))
        
@login_required
def delete(request, auction_id):
    a = AuctionListing.objects.get(id= auction_id)
    a.startbid.winner = True
    a.startbid.save()
    return HttpResponseRedirect(reverse('auction', args=(auction_id,)))

@login_required
def comment(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['user'])
        auction = AuctionListing.objects.get(title=request.POST['auction'])
        comment = Comment(user=user, comment=request.POST['comment'])
        comment.save()
        auction.comment.add(comment)
        return HttpResponseRedirect(reverse('auction', args=(auction.id,)))

def category(request):
    auction = AuctionListing.objects.all()
    return render(request, 'auctions/category.html',{
        'category': auction
    })

def filter(request, filter_id):
    auc = AuctionListing.objects.filter(category=filter_id)
    return render(request, 'auctions/filter.html',{
        'auc': auc,
        'name': filter_id
    })