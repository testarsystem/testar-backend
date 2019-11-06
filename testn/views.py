from rest_framework.viewsets import ModelViewSet
from . import serializers
from .models import Test
from testar.mixins import ActionSerializerClassMixin, SetOwnerMixin


class TestViewSet(ActionSerializerClassMixin, SetOwnerMixin, ModelViewSet):
    action_serializer_class = {
        "create": serializers.TestCreatingSerializer
    }
    serializer_class = serializers.TestSerializer

    def get_queryset(self):
        return Test.objects.filter(owner=self.request.payload['id'])
