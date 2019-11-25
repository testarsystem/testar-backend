from public.models import PublicCompetition
from public.serializers import PublicCompetitionSerializer, PublicTestSerializer, SubmissionSerializer
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from testar.exceptions import BaseException
from competition.models import Participant

#todo make method that checks if competition is still active and participants can join and submit
class PublicCompetitionViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):

    filter_backends = (SearchFilter,)
    search_fields = ('title',)
    serializer_class = PublicCompetitionSerializer

    def get_queryset(self):
        # todo: sort by time
        return PublicCompetition.objects.all()

    @action(['GET'], detail=True, url_path='test', url_name='competition_test')
    def test(self, *args, **kwargs):
        # todo: filter by time (not started, not finished), if not participant not show
        pk = kwargs['pk']
        competition = self.__get_competition(pk)
        test_serializer = PublicTestSerializer(instance=competition.test)
        return Response(data=test_serializer.data)

    @action(('POST',), detail=True, url_path='join', url_name='competition_join')
    def join(self, request, pk):
        competition = self.__get_competition(pk)
        participant = Participant.objects.filter(competition=competition, user=request.user).first()
        if not participant:
            Participant.objects.create(competition=competition,
                                       user=request.user,
                                       owner=competition.owner)
        return Response(status=200)

    @action(('POST',), detail=True, url_path='submit', url_name='competition_submit')
    def submission(self, request, pk):
        # todo: check if question, answer related to test
        competition = self.__get_competition(pk)
        participant = self.__get_participant(competition, request)
        submission_serializer = SubmissionSerializer(data=request.data)
        submission_serializer.is_valid(True)
        # todo: check uniqueness for certain question and answer
        submission_serializer.save(participant=participant, test=competition.test)
        return Response(status=200)

    @staticmethod
    def __get_competition(pk):
        competition = PublicCompetition.objects.filter(id=pk).first()
        if not competition:
            raise BaseException(status=404, detail='competition not found', code='not_found')
        return competition

    @staticmethod
    def __get_participant(competition, request):
        participant = Participant.objects.filter(competition=competition, user=request.user).first()
        if not participant:
            raise BaseException(status=403, detail='you are not participant', code='not_participant')
        return participant