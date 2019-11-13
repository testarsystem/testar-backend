from django.shortcuts import render
from authn.models import User
from authn.serializers import UserSerializer
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter


class PublicUserViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    authentication_classes = ()
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

