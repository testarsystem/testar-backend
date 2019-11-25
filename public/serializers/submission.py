from rest_framework.serializers import ModelSerializer
from competition.models import Submission


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('question', 'answer')

