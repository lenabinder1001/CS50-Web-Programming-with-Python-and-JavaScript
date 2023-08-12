from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=60, blank=False)

    def __str__(self):
        return f"{self.name}"
    
class List(models.Model):
    name = models.CharField(max_length=60, blank=False)

    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    title = models.CharField(max_length=200, blank=False)
    author = models.CharField(max_length=200, blank=False)
    content = models.TextField(max_length=1000, blank=False, default=0)
    rating = models.IntegerField(default=0, null=False)
    pages = models.IntegerField(default=0, null=False)
    image = models.CharField(default=0, max_length=300)
    read = models.BooleanField(default=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.title} from {self.author}"
    
class Goal(models.Model):
    books = models.IntegerField(default=0, null=False)
    pages = models.IntegerField(default=0, null=False)

    def __str__(self):
        return f"{self.books}, {self.pages}"