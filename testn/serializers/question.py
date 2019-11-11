from testn import models
from rest_framework import serializers
from .answer import AnswerSerializer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('id', 'text', 'created', 'answers')

    answers = AnswerSerializer(many=True)


class QuestionCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('id', 'text')
