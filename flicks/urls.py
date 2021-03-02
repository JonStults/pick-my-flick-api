from django.urls import path
from flicks.views.movies import MoviesView
from flicks.views.genres import GenresView
from flicks.views.random import RandomView

urlpatterns = [
    path("movies", MoviesView.as_view()),
    path("genres", GenresView.as_view()),
    path("random", RandomView.as_view()),
]

