# Generated by Django 3.1.5 on 2021-02-07 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210206_2259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='auction',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='auction',
            field=models.ManyToManyField(blank=True, related_name='auctioniw', to='auctions.AuctionListing'),
        ),
    ]