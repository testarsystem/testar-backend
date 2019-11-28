from rest_framework import serializers as s
from competition.models import Submission


class SubmissionSerializer(s.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'question', 'answer')


class DeleteSubmissionSerializer(s.Serializer):
    id = s.IntegerField(required=True)