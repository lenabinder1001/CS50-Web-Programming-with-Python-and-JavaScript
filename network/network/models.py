from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=True)

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def get_followed_posts(self):
        return self.user_followed.posts.order_by('-timestamp').all()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,  on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
