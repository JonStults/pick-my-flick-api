from django.shortcuts import render, redirect
import json
import string
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from django.views import View
from rest_framework import status
from ..models import User
import jwt
from django.core import serializers
import hashlib


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request):
        response = dict()
        statusCode = status.HTTP_200_OK
        try:
            print("LOGIN")
            data = json.loads(request.body)
            user = User.objects.filter(username=data["username"])
            if not user:
                raise Exception("Username does not exist.")
            else:
                t_hashed = hashlib.sha256(data["password"].encode())
                t_password = t_hashed.hexdigest()
                user = json.loads(serializers.serialize("json", user))
                id = user[0]["pk"]
                user = user[0]["fields"]
                if user["password"] == t_password:
                    payload = {
                        "id": id,
                        "username": user["username"],
                    }
                    payload["exp"] = datetime.now() + timedelta(days=30)
                    en = jwt.encode(payload, "secret", algorithm="HS256")
                    response["token"] = en
                    response["ok"] = True
                else:
                    raise Exception("Incorrect password.")
        except Exception as e:
            statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["message"] = "INTERNAL_SERVER_ERROR"
            response["detail"] = str(e)
        response = json.dumps(response, default=lambda x: x.__dict__)
        return HttpResponse(
            response, status=statusCode, content_type="application/json"
        )
