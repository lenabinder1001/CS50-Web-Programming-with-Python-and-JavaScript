# Generated by Django 3.2.5 on 2023-02-05 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_like'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
