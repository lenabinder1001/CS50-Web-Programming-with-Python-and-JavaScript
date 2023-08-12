from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.all_listings, name="all_listings"),
    path("all_listings", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:user_id>/create", views.create_listing, name="create_listing"),
    path('<int:user_id>/watchlist', views.watchlist, name="watchlist"),
    path("<int:listing_id>/bid/<int:user_id>", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path('<int:listing_id>/', views.listing, name="listing"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("<int:user_id>/comment/<int:listing_id>", views.comment, name="comment"),
    path('<int:category_id>/detail', views.category_detail, name="category_detail"),
    path('<int:user_id>/watchlist/add/<int:listing_id>', views.watchlist_add, name="watchlist_add"),
    path('<int:user_id>/watchlist/remove/<int:listing_id>', views.watchlist_remove, name="watchlist_remove"),
]
