from rest_framework import serializers
from . import models


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'text', 'correct', 'created')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('id', 'text', 'created', 'answers')

    answers = AnswerSerializer(many=True)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = ('id', 'title', 'description', 'created', 'questions')

    questions = QuestionSerializer(many=True)


class TestCreatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = ('id', 'title', 'description')
