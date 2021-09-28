from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)


class Genre(models.Model):
    genre = models.CharField(max_length=100, blank=True, null=True)


class Movie(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    poster_path = models.CharField(max_length=255, blank=False, null=True)
    overview = models.TextField(blank=False, null=False)
    genre_ids = models.CharField(max_length=255, blank=False, null=False)
    release_date = models.CharField(max_length=50, blank=False, null=False)

class UserFlick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=False, related_name="movie")
    watched = models.BooleanField(default=False)

