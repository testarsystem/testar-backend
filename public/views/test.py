from public.models import PublicCompetition
from public.serializers import PublicCompetitionSerializer
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter


class PublicCompetitionViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):

    filter_backends = (SearchFilter,)
    search_fields = ('title',)
    serializer_class = PublicCompetitionSerializer

    def get_queryset(self):
        # todo: sort by time
        return PublicCompetition.objects.all()

