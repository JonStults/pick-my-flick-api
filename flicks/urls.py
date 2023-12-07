from flicks.views.movieGenres import GetGenres
from flicks.views.searchMovies import SearchMovies
from django.urls import path
from flicks.views.movies import MoviesView
from flicks.views.genres import GenresView
from flicks.views.random import RandomView
from flicks.views.login import LoginView
from flicks.views.register import RegisterView
from flicks.views.userFlick import UserFlickView
from flicks.views.searchMovies import SearchMovies

urlpatterns = [
    path("login", LoginView.as_view()),
    path("register", RegisterView.as_view()),
    path("movies", MoviesView.as_view()),
    path("genres", GenresView.as_view()),
    path("random", RandomView.as_view()),
    path("userFlick", UserFlickView.as_view()),
    path("searchMovies", SearchMovies.as_view()),
    path("getGenres", GetGenres.as_view())
]

