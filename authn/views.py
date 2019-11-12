
from rest_framework.views import APIView


from .serializers import LoginSerializer, RegistrationSerializer
from django.contrib.auth import authenticate
from . import error_codes as ec

from testar.exceptions import BaseException
from rest_framework import status, viewsets, mixins
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



class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegistrationSerializer
    authentication_classes = ()
    permission_classes = ()
