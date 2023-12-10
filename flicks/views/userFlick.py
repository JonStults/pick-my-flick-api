import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from flicks.serializers import MovieSerializer, UserFlickSerializer
from rest_framework import status
from ..models import Movie, User, UserFlick

@method_decorator(csrf_exempt, name="dispatch")
class UserFlickView(View):
    def get(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try: 
            userId = request.GET.get("userId")
            if userId is None:
                raise ValueError("User ID is missing in the request.")
           
            movieId = request.GET.get("movieId")
            if movieId is None:
                raise ValueError("Movie ID is missing in the request.")
            
            user = User.objects.filter(id=userId).first()
            existingMovie = Movie.objects.filter(id=movieId)
            existingUserFlick = UserFlick.objects.filter(user=user, movie=existingMovie.first())

            if not existingUserFlick.exists():
                # Handle the case where no matching record is found
                print("No matching record found.")
                response["ok"] = False
                response["message"] = "Movie ID not found."
                statusCode = status.HTTP_404_NOT_FOUND
            else:
                serializer = UserFlickSerializer(existingUserFlick.first(), many=False)
                response["ok"] = True
                response = serializer.data
        except UserFlick.DoesNotExist:
            print("No matching record found.")
            response["ok"] = False
            response["message"] = "Movie ID not found."
            statusCode = status.HTTP_404_NOT_FOUND
        except ValueError as ve:
            statusCode = status.HTTP_400_BAD_REQUEST
            response["status"] = status.HTTP_400_BAD_REQUEST
            response["message"] = "BAD_REQUEST"
            response["detail"] = str(ve)
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
            user_flick = UserFlick(user=user, movie=movie)
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

    def put(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            data = json.loads(request.body)
            user_id = data["userId"]
            movie_id = data["movieId"]
            watched = data["watched"]
            UserFlick.objects.filter(movie=movie_id, user=user_id).update(watched=watched)
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
