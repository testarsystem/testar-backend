from django.shortcuts import render
from rest_framework import viewsets, mixins
from testar.mixins import SetOwnerMixin, ActionSerializerClassMixin
from competition import serializers, models
from testar.exceptions import BaseException


class CompetitionViewSet(SetOwnerMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CompetitionSerializer

    def get_queryset(self):
        return self.request.user.competitions.all()


class ParticipantsViewSet(ActionSerializerClassMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    action_serializer_class = {
        "create": serializers.ParticipantCreationSerializer
    }
    serializer_class = serializers.ParticipantSerializer

    def perform_create(self, serializer):
        competition = models.Competition.objects.filter(id=self.kwargs['competition_pk'], owner=self.request.user).first()
        if not competition:
            raise BaseException(status=404, detail='competition not found', code='not_found')
        serializer.save(owner=self.request.user, competition=competition)

    def get_queryset(self):
        return self.request.user.participants.filter(competition_id=self.kwargs['competition_pk']).all()


