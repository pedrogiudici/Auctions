from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create, name='create'),
    path('addwatchlist', views.addwatchlist, name='addwatchlist'),
    path('bid', views.bid, name='bid'),
    path('comment', views.comment, name='comment'),
    path('category', views.category, name='category'),
    path('<str:filter_id>/filter', views.filter, name='filter'),
    path('<str:auction_id>/delete', views.delete, name='delete'),
    path('<str:user_username>/watchlist', views.watchlist, name='watchlist'),
    path('<int:auction_id>', views.auction, name='auction')
]
