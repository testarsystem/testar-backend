from testn.serializers import TestSerializer, QuestionSerializer, AnswerSerializer
from rest_framework.serializers import ModelSerializer
from testn.models import Answer


class PublicAnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ('text',)


class PublicQuestionSerializer(QuestionSerializer):
    answers = PublicAnswerSerializer(many=True)


class PublicTestSerializer(TestSerializer):
    questions = PublicQuestionSerializer(many=True)
