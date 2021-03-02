import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from ..models import Genre
from ..serializers import GenreSerializer


@method_decorator(csrf_exempt, name="dispatch")
class GenresView(View):
    def get(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            genre_list = list()
            genres = Genre.objects.all()
            for g in genres:
                serializer = GenreSerializer(g)
                genre_list.append(serializer.data["genre"])
            response["genres"] = genre_list
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
