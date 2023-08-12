from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from itertools import chain
from django.core.paginator import Paginator
import json

from .models import User, Post, Following, Like


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    likes = Like.objects.filter(user=request.user.id).values_list('post_id', flat=True)
    liked_posts = Post.objects.filter(id__in=likes)
    return render(request, "network/index.html", {"posts" : posts, 'liked_posts': liked_posts, 'likes': likes, 'page_posts': page_posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create(request):
    if request.method == "POST":
        text = request.POST["post"]
        user = User.objects.get(pk=request.user.id)
        post = Post.objects.create(text=text, user=user)
        post.save()
        return redirect('index')

def profile(request, user_id):
    user_data = User.objects.get(pk=user_id)
    posts = user_data.posts.order_by('timestamp').all()
    followers_id_list = Following.objects.filter(user_followed=user_id).values_list('user_id', flat=True)
    followers_user_list = User.objects.filter(id__in=followers_id_list)
    likes = Like.objects.filter(user=request.user.id).values_list('post_id', flat=True)
    liked_posts = Post.objects.filter(id__in=likes)

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)

    return render(request, "network/user.html", {"user_data" : user_data, "posts": posts, "page_posts": page_posts, "followers": followers_user_list, 'liked_posts': liked_posts, 'likes': likes})

def follow_unfollow(request, user_id):
    user_data = User.objects.get(pk=user_id)
    posts = user_data.posts.order_by('timestamp').all()
    followers_id_list = Following.objects.filter(user_followed=user_id).values_list('user_id', flat=True)
    followers_user_list = User.objects.filter(id__in=followers_id_list)
    if request.method == "POST":
        try:
            get_followers = Following.objects.get(user=request.user, user_followed=user_id)
        except Following.DoesNotExist:
            try:
                user_to_follow = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return HttpResponse(statu=404)
            else:
                new_follower = Following.objects.create(user=request.user, user_followed=user_to_follow)
                new_follower.save()
        else:
            get_followers.delete()
            
        # Pagination
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_posts = paginator.get_page(page_number)

        return render(request, "network/user.html", {"user_data" : user_data, "posts": posts, "page_posts": page_posts, "followers": followers_user_list})

def following(request):
    user = User.objects.get(pk=request.user.id)
    posts = [users.get_followed_posts() for users in user.following.all()]
    posts = list(chain(*posts))
    likes = Like.objects.filter(user=request.user.id).values_list('post_id', flat=True)
    liked_posts = Post.objects.filter(id__in=likes)

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_posts = paginator.get_page(page_number)
    return render(request, "network/following.html", {"posts": posts, "page_posts": page_posts, 'liked_posts': liked_posts, 'likes': likes})

def edit(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        data = json.loads(request.body)
        if data.get("text") is not None:
            post.text = data["text"]
        post.save()
        return JsonResponse({"message": "Change successful!"})

def unlike(request, post_id):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=post_id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"message": "Unliked!"})

def like(request, post_id):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=post_id)
    new_like = Like.objects.create(user=user, post=post)
    new_like.save()
    return JsonResponse({"message": "Liked!"})
