from rest_framework.viewsets import ModelViewSet
from . import serializers
from . import models
from testar.mixins import ActionSerializerClassMixin, SetOwnerMixin
from testar.exceptions import BaseException


class TestViewSet(ActionSerializerClassMixin, SetOwnerMixin, ModelViewSet):
    action_serializer_class = {
        "create": serializers.TestCreatingSerializer
    }
    serializer_class = serializers.TestSerializer

    def get_queryset(self):
        return models.Test.objects.filter(owner=self.request.payload['id'])


class QuestionViewSet(ActionSerializerClassMixin, ModelViewSet):
    action_serializer_class = {
        "create": serializers.QuestionCreationSerializer
    }
    serializer_class = serializers.QuestionSerializer

    def get_queryset(self):
        return models.Question.objects.filter(owner=self.request.payload['id'], test_id=self.kwargs['test_pk'])

    def perform_create(self, serializer):
        test = models.Test.objects.filter(owner=self.request.payload['id'], id=self.kwargs['test_pk']).first()
        if not test:
            raise BaseException(status=404, detail='test not found')
        serializer.save(test=test, owner=self.request.user)
