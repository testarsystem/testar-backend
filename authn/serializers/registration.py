from authn.models import User
from rest_framework import serializers as s
from authn.utils import login_response
from .user import UserSerializer


class RegistrationSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'name')

    def create(self, validated_data):
        user = User(username=validated_data['username'], name=validated_data.get('name'))
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        user_serializer = UserSerializer
        payload, token = instance.login()
        return {
            "token": token,
            "user": user_serializer(instance=instance).data,
            "payload": payload
        }

