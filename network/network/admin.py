from django.contrib import admin
from .models import User, Post, Following, Profile, Like

# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Following)
admin.site.register(Profile)
admin.site.register(Like)
