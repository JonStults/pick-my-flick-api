import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from ..models import Movie, User, UserFlick

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
            user_flick = UserFlick.objects.filter(movie=movie_id, user=user_id)

            if user_flick:
                # Update the watched attribute
                user_flick.watched = watched
                user_flick.save()
            else:
                # Handle the case where the UserFlick instance doesn't exist
                statusCode = status.HTTP_404_NOT_FOUND
                response["status"] = status.HTTP_404_NOT_FOUND
                response["message"] = "UserFlick instance not found."    
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
