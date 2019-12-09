from rest_framework import serializers as s
from competition import models
from authn.serializers import UserSerializer


class CompetitionSerializer(s.ModelSerializer):
    class Meta:
        model = models.Competition
        fields = ('id', 'title', 'description', 'created', 'start_time', 'finish_time', 'duration', 'test')

    def validate(self, attrs):
        if attrs['finish_time'] <= attrs['start_time']:
            raise s.ValidationError(detail={"finish_time": "finish_time must be greater than start_time"})
        return attrs


class ParticipantSerializer(s.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = ('id', 'user', 'start_time', 'end_time', 'points')
    user = UserSerializer()


class ParticipantCreationSerializer(s.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = ('user',)
