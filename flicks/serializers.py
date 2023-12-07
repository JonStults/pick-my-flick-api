from requests import NullHandler
from rest_framework import serializers
from .models import Movie, Genre, UserFlick


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["genre"]


class GenreField(serializers.RelatedField):
    def to_representation(self, value):
        return value.genre


class TitleField(serializers.CharField):
    def to_representation(self, value):
        return value.title()


class WatchedField(serializers.BooleanField):
    def to_representation(self, value):
        return value.watched


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ["title", "poster_path",
                  "genre_ids", "id", "overview", "release_date"]


class UserFlickSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFlick
        fields = ["watched", "movie"]

    movie = MovieSerializer(many=False)


class SearchedMovie:
    def __init__(self, data):
        self.title = data["title"]
        self.genre_ids = data["genre_ids"]
        self.id = data["id"]
        self.overview = data["overview"]
        self.poster_path = data["poster_path"] if "poster_path" in data else ""
        self.release_date = data["release_date"] if "release_date" in data else ""
        self.text = data["title"]
        self.value = data["id"]
        self.key = data["id"]

class MovieGenres:
    def __init__(self, data):
        self.name = data["name"]
        self.id = data["id"]
        self.key = data["id"]
