from testn import models
from rest_framework import serializers
from .question import QuestionSerializer


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = ('id', 'title', 'description', 'created', 'questions')

    questions = QuestionSerializer(many=True)


class TestCreatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = ('id', 'title', 'description')
