from rest_framework import serializers as s
from competition import models
from authn.serializers import UserSerializer


class CompetitionSerializer(s.ModelSerializer):
    class Meta:
        model = models.Competition
        fields = ('id', 'title', 'description', 'created', 'start_time', 'finish_time', 'duration', 'test')


class ParticipantSerializer(s.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = ('id', 'user', 'start_time', 'end_time')
    user = UserSerializer()


class ParticipantCreationSerializer(s.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = ('user',)
