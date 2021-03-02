import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import random
from rest_framework import status
from ..models import Movie, Genre
from ..serializers import MovieSerializer


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
            genre = Genre.objects.filter(genre=data["genre"]).first()
            new_movie = Movie(title=data["title"], genre=genre)
            new_movie.save()
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
