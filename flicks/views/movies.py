import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from ..models import Movie, User, UserFlick
from ..serializers import MovieSerializer, UserFlickSerializer

@method_decorator(csrf_exempt, name="dispatch")
class MoviesView(View):
    def get(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            user_id = request.GET.get("userId")
            user = User.objects.filter(id=user_id).first()
            movie_list = list()
            user_flick_movies =  UserFlick.objects.filter(user=user.id).select_related("movie")
            for movie in user_flick_movies:
                serializer = UserFlickSerializer(movie)
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

    def post(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            data = json.loads(request.body)
            movie_data = data["data"]
            title = movie_data["title"]
            existing_movie = Movie.objects.filter(id=movie_data["id"])
            user = User.objects.filter(id=data["userId"]).first()
            existing_user_flick = UserFlick.objects.filter(user=user, movie=existing_movie.first())
            if not existing_movie:
                new_movie = Movie(id=movie_data["id"], title=title, poster_path=movie_data["poster_path"],
                                  overview=movie_data["overview"], genre_ids=movie_data["genre_ids"],
                                  release_date=movie_data["release_date"])
                new_movie.save()
                user_flick = UserFlick(user=user, movie=new_movie)
                user_flick.save()
            elif not existing_user_flick:
                user_flick = UserFlick(
                    user=user, movie=existing_movie.first())
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
