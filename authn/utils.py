
from .serializers import UserSerializer
from rest_framework.response import Response


def login_response(user):
    user_serializer = UserSerializer
    payload, token = user.login()
    return Response({
        "token": token,
        "user": user_serializer(instance=user).data,
        "payload": payload
    })