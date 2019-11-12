from rest_framework.viewsets import ModelViewSet
from . import serializers
from . import models
from testar.mixins import ActionSerializerClassMixin, SetOwnerMixin
from testar.exceptions import BaseException


class TestViewSet(ActionSerializerClassMixin, SetOwnerMixin, ModelViewSet):
    action_serializer_class = {
        "retrieve": serializers.TestSerializer
    }
    serializer_class = serializers.TestCreatingSerializer

    def get_queryset(self):
        return models.Test.objects.filter(owner=self.request.payload['id'])


class QuestionViewSet(ActionSerializerClassMixin, ModelViewSet):
    action_serializer_class = {
        "retrieve": serializers.QuestionSerializer
    }
    serializer_class = serializers.QuestionCreationSerializer

    def get_queryset(self):
        return models.Question.objects.filter(owner=self.request.payload['id'], test_id=self.kwargs['test_pk'])

    def perform_create(self, serializer):
        test = models.Test.objects.filter(owner=self.request.payload['id'], id=self.kwargs['test_pk']).first()
        if not test:
            raise BaseException(status=404, detail='test not found', code='not_found')
        serializer.save(test=test, owner=self.request.user)


class AnswerViewSet(ActionSerializerClassMixin, ModelViewSet):
    serializer_class = serializers.AnswerSerializer

    def get_queryset(self):
        return models.Answer.objects.filter(owner=self.request.payload['id'], question_id=self.kwargs['question_pk'])

    def perform_create(self, serializer):
        question = models.Question.objects.filter(owner=self.request.payload['id'], id=self.kwargs['question_pk']).first()
        if not question:
            raise BaseException(status=404, detail='question not found', code='not_found')
        serializer.save(owner=self.request.user, question=question)
