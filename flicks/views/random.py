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
class RandomView(View):
    def get(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            random_number_list = set()
            movie_list = list()
            movie_length = len(Movie.objects.all())
            while len(random_number_list) < int(request.GET.get("number")):
                random_number = random.randint(1, movie_length)
                random_number_list.add(random_number)
            movies = Movie.objects.filter(id__in=random_number_list)
            for movie in movies:
                serializer = MovieSerializer(movie)
                movie_list.append(serializer.data)
            response = movie_list
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
