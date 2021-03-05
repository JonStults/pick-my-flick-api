import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import random
from rest_framework import status
from ..models import Movie, Genre, UserFlick, User
from ..serializers import MovieSerializer


@method_decorator(csrf_exempt, name="dispatch")
class RandomView(View):
    def get(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            user_id = request.GET.get("userId")
            random_number_list = set()
            movie_list = list()
            movie_length = len(Movie.objects.all())
            retrieve_number = (
                movie_length
                if movie_length < int(request.GET.get("number"))
                else int(request.GET.get("number"))
            )
            if retrieve_number > 0:
                user = User.objects.filter(id=user_id).first()
                id_list = UserFlick.objects.filter(user=user.id).values_list(
                    "movie_id", flat=True
                )
                random_list = random.sample(
                    list(id_list), min(len(id_list), retrieve_number)
                )
                movies = Movie.objects.filter(id__in=random_list)
                for movie in movies:
                    serializer = MovieSerializer(movie)
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
