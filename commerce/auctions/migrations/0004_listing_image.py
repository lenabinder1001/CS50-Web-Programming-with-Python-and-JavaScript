# Generated by Django 3.2.5 on 2023-01-04 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20230104_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.CharField(default=0, max_length=300),
        ),
    ]