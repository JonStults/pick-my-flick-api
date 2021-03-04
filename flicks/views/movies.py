import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import random
from rest_framework import status
from ..models import Movie, Genre, User, UserFlick
from ..serializers import MovieSerializer
from django.db.models.functions import Lower
import re


@method_decorator(csrf_exempt, name="dispatch")
class MoviesView(View):
    def get(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            movie_list = list()
            movies = Movie.objects.all()
            for movie in movies:
                serializer = MovieSerializer(movie)
                movie_list.append(serializer.data)
            response = movie_list
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )

    def post(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            data = json.loads(request.body)
            upperCaseTitle = data["title"].upper()
            existing_movie = Movie.objects.filter(title=upperCaseTitle)
            user = User.objects.filter(id=data["userId"]).first()
            if existing_movie:
                raise Exception(
                    f"{existing_movie.first().title.title()} is already in the Pick My Flick db. Add this movie to your list?"
                )
            if len(data["title"]) >= 5:
                split_title = upperCaseTitle.split()
                for s in split_title:
                    existing_string = Movie.objects.filter(title__contains=s.upper())
                    if existing_string:
                        response["message"] = (
                            "Did you mean "
                            + existing_string.first().title.title()
                            + "?"
                        )
                        response["ok"] = False
                        response = json.dumps(response, default=lambda x: x.__dict__)
                        return HttpResponse(
                            response, status=statusCode, content_type="application/json"
                        )
            response["message"] = ""
            response["ok"] = True
            genre = Genre.objects.filter(genre=data["genre"]).first()
            new_movie = Movie(title=upperCaseTitle, genre=genre)
            new_movie.save()
            user_flick = UserFlick(user=user, movie=new_movie)
            user_flick.save()
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
