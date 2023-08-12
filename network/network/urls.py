
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("following", views.following, name="following"),
    path("<int:post_id>/edit", views.edit, name="edit"),
    path("<int:post_id>/unlike", views.unlike, name="unlike"),
    path("<int:post_id>/like", views.like, name="like"),
    path("<int:user_id>/profile", views.profile, name="profile"),
    path("<int:user_id>/follow-unfollow", views.follow_unfollow, name="follow-unfollow"),
    path("<int:post_id>/edit", views.edit, name="edit"),
]
