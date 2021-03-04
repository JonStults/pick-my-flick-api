from django.urls import path
from flicks.views.movies import MoviesView
from flicks.views.genres import GenresView
from flicks.views.random import RandomView
from flicks.views.login import LoginView
from flicks.views.register import RegisterView

urlpatterns = [
    path("login", LoginView.as_view()),
    path("register", RegisterView.as_view()),
    path("movies", MoviesView.as_view()),
    path("genres", GenresView.as_view()),
    path("random", RandomView.as_view()),
]

