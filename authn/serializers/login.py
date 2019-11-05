from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    testar = serializers.CharField()
    password = serializers.CharField()
