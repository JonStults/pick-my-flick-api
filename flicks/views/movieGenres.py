import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import requests
import os
import random
from rest_framework import status
from ..serializers import  MovieGenres
from dotenv import load_dotenv


@method_decorator(csrf_exempt, name="dispatch")
class GetGenres(View):
    def get(self, _):
        load_dotenv()
        MOVIES_DB_BEARER_TOKEN = os.getenv("MOVIES_DB_BEARER_TOKEN")
        genres_list = list()
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

            headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {MOVIES_DB_BEARER_TOKEN}"
            }
            api_response = requests.request("GET", url, headers=headers)
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
