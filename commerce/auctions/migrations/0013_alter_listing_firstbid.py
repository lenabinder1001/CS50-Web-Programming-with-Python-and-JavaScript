# Generated by Django 3.2.5 on 2023-01-13 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_listing_firstbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='firstBid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
