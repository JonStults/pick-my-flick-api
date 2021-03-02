from django.db import models

# Create your models here.


class Genre(models.Model):
    genre = models.CharField(max_length=100, blank=True, null=True)


class Movie(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    watched = models.BooleanField(default=False, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

