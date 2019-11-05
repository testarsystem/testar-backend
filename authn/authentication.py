from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions, status
from authn import jwt_utils
from .models import User
from authn import error_codes as ec
from testar.exceptions import BaseException


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = jwt_utils.get_jwt_value(request)
        payload = jwt_utils.get_payload(token)
        if not payload.get('id'):
            msg = 'Invalid payload'
            raise BaseException(msg, code=ec.INVALID, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'Invalid signature'
            raise BaseException(msg, code=ec.INVALID, status=status.HTTP_403_FORBIDDEN)
        if not user.is_active:
            msg = 'User account is disabled'
            raise BaseException(msg, code=ec.INVALID, status=status.HTTP_403_FORBIDDEN)
        request.payload = payload
        request.token = token
        return user, token

