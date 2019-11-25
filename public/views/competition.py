from public.models import PublicCompetition
from public.serializers import PublicCompetitionSerializer, PublicTestSerializer
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from testar.exceptions import BaseException


class PublicCompetitionViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):

    filter_backends = (SearchFilter,)
    search_fields = ('title',)
    serializer_class = PublicCompetitionSerializer

    def get_queryset(self):
        # todo: sort by time
        return PublicCompetition.objects.all()

    @action(['GET'], detail=True, url_path='test', url_name='public_competition_test')
    def competition_test(self, *args, **kwargs):
        # todo: filter by time (not started, not finished)
        pk = kwargs['pk']
        competition = PublicCompetition.objects.filter(id=pk).first()
        if not competition:
            raise BaseException(status=404, detail='competition not found', code='not_found')
        test_serializer = PublicTestSerializer(instance=competition.test)
        return Response(data=test_serializer.data)


