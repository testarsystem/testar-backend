from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions as exc
from . import error_codes as ec
from .serializers import UserSerializer

from testar.exceptions import BaseException
from rest_framework import status
from .utils import login_response



class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(True)
        username = login_serializer.data['testar']
        password = login_serializer.data['password']
        user = authenticate(request, username=username, password=password)
        if not user:
            raise BaseException('unable to login with given credentials', code=ec.INVALID,
                                 status=status.HTTP_401_UNAUTHORIZED)
        return login_response(user)


class TokenInfoView(APIView):
    def get(self, request):
        return login_response(request.user)

