from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions, status
from . import error_codes as ec
from django.conf import settings
import jwt
import base64
from time import time as now
from testar.exceptions import BaseException


def get_jwt_value_from_headers(request, prefix='Bearer '):
    auth = get_authorization_header(request).decode()
    if not auth:
        return None
    if prefix and auth.startswith(prefix):
        auth = auth[len(prefix):]
    return auth


def get_jwt_value_from_data(request):
    return request.data.get('token')


def get_jwt_value_from_query(request):
    return request.query_params.get('token')


def get_jwt_value(request):
    token = get_jwt_value_from_headers(request) or get_jwt_value_from_data(request) or get_jwt_value_from_query(request)
    if not token:
        raise BaseException('authentication credentials not provided', code=ec.INVALID,
                             status=status.HTTP_401_UNAUTHORIZED)
    return token.decode() if isinstance(token, bytes) else token


def get_payload(token):
    try:
        jwt_token = base64.b64decode(token)
    except Exception as e:
        raise BaseException('invalid token', code=ec.INVALID, status=status.HTTP_401_UNAUTHORIZED)

    try:
        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithm='HS256')
    except jwt.exceptions.ExpiredSignature:
        raise BaseException('token expired', code=ec.TOKEN_EXPIRED, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.DecodeError:
        raise BaseException('invalid token', code=ec.INVALID, status=status.HTTP_401_UNAUTHORIZED)
    return payload


def generate_token(payload: dict):
    payload['exp'] = now() + settings.TOKEN_EXPIRATION_TIME
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return base64.b64encode(jwt_token)
    



