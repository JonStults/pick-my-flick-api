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
from ..serializers import  MovieGenres
from dotenv import load_dotenv
from django.db.models.functions import Lower
import re


@method_decorator(csrf_exempt, name="dispatch")
class GetGenres(View):
    def get(self, request):
        load_dotenv()
        API_KEY = os.getenv("MOVIES_DB_API_KEY")
        genres_list = list()
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            print('GET MOVIE GENRES')
            url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

            headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNWE3MjkzMjg3MzA4MDY0OWU4M2ZmNzRhMDBhMjZkNiIsInN1YiI6IjY1NmZiODlmOTQ2MzE4MDEwMGM2YmE4ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.37AzMiibDDo_bX1TMRmOeBJ-JwDHQFk1b8U9vEocq-Y"
            }
            api_response = requests.request("GET", url, headers=headers)
            print('----')
            print(api_response.json())
            print('----')
            for r in api_response.json()["genres"]:
                genres_list.append(MovieGenres(r))
            response["message"] = ""
            response["ok"] = True
            response["results"] = genres_list
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)

        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
