from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)


class Genre(models.Model):
    genre = models.CharField(max_length=100, blank=True, null=True)


class Movie(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    watched = models.BooleanField(default=False, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)


class UserFlick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=False)
    watched = models.BooleanField(default=False)

