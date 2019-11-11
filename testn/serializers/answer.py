from testn import models
from rest_framework import serializers


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'text', 'correct',)

