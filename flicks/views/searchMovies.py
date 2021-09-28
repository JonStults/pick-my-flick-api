import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import requests
import os
import random
from rest_framework import status
from ..models import Movie, Genre, User, UserFlick
from ..serializers import MovieSerializer, SearchedMovie
from dotenv import load_dotenv
from django.db.models.functions import Lower
import re


@method_decorator(csrf_exempt, name="dispatch")
class SearchMovies(View):
    def get(self, request):
        load_dotenv()
        API_KEY = os.getenv("MOVIES_DB_API_KEY")
        movie_list = list()
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            title = request.GET.get('title')
            page = request.GET.get('page')
            url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=en-US&query={title}&page={page}"
            api_response = requests.request("GET", url)
            for r in api_response.json()["results"]:
                movie_list.append(SearchedMovie(r))
            print('----')
            print(api_response.json())
            print('----')
            response["message"] = ""
            response["ok"] = True
            response["movie_list"] = movie_list
            response["total_pages"] = api_response.json()["total_pages"]
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
