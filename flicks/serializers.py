from rest_framework import serializers
from .models import Movie, Genre


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


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreField(read_only=True)
    title = TitleField(read_only=True)

    class Meta:
        model = Movie
        fields = ["title", "watched", "genre"]
