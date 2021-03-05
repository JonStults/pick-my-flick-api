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
class UserFlickView(View):
    def post(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            data = json.loads(request.body)
            user = User.objects.filter(id=data["userId"]).first()
            movie = Movie.objects.filter(id=data["movieId"]).first()
            userFlick = UserFlick.objects.filter(movie=movie.id, user=user.id)
            if userFlick:
                response["metaMessage"] = "Movie already in user list."
                response["ok"] = True
                response = json.dumps(response, default=lambda x: x.__dict__)
                return HttpResponse(
                    response, status=statusCode, content_type="application/json"
                )
            user_flick = UserFlick(user=user, movie=new_movie)
            user_flick.save()
            response["message"] = ""
            response["ok"] = True
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
