import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import random
from rest_framework import status
from ..models import Movie, UserFlick, User
from ..serializers import  UserFlickSerializer


@method_decorator(csrf_exempt, name="dispatch")
class RandomView(View):
    def get(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            user_id = request.GET.get("userId")
            user = User.objects.filter(id=user_id).first()
            movie_list = list()
            # user_flicks = UserFlick.objects.filter(user=user.id)
            user_flick_movies =  UserFlick.objects.filter(user=user.id).select_related("movie")
            movie_length = len(user_flick_movies)
            retrieve_number = (
                movie_length
                if movie_length < int(request.GET.get("number"))
                else int(request.GET.get("number"))
            )
            if retrieve_number > 0:
                id_list = user_flick_movies.values_list(
                    "id", flat=True
                )
                random_list = random.sample(
                    list(id_list), min(len(id_list), retrieve_number)
                )
                movies = user_flick_movies.filter(id__in=random_list)
                # userFlicks = UserFlick.objects.filter(user_id=user_id)
                for movie in movies:
                    serializer = UserFlickSerializer(movie)
                    # serializer["watched"] = userFlicks.filter(movie_id=movie["id"])
                    movie_list.append(serializer.data)
                response = movie_list
            else:
                raise Exception("No movies in user list.")
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
