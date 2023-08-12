from django.contrib import admin

from .models import Genre, List, Book, Goal

admin.site.register(Genre)
admin.site.register(List)
admin.site.register(Book)
admin.site.register(Goal)
