from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('create', views.create, name="create"),
    path('goals', views.goals, name="goals"),
    path('genres', views.genres, name="genres"),
    path('profile', views.profile, name="profile"),
    path('search', views.search, name="search"),
    path('genre/<int:genre_id>', views.genre, name="genre"),
    path('list/<int:list_id>', views.list, name="list"),
    path('book/<int:book_id>', views.book, name="book"),
    path('book/edit/<int:book_id>', views.edit, name="edit"),
    path('book/delete/<int:book_id>', views.delete, name="delete"),
    path('book/read-unread/<int:book_id>', views.read_unread, name="read_unread"),
    path('book/bookshelf_wishlist/<int:book_id>', views.bookshelf_wishlist, name="bookshelf_wishlist"),
]