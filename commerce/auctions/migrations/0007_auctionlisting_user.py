# Generated by Django 3.1.5 on 2021-02-06 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auctionlisting'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='user',
            field=models.CharField(default='PADRAO', max_length=64),
        ),
    ]
