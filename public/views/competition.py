from public.models import PublicCompetition
from public.serializers import PublicCompetitionSerializer, PublicTestSerializer, SubmissionSerializer, DeleteSubmissionSerializer
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from testar.exceptions import BaseException
from competition.models import Participant, Submission, Competition
from competition.utils import calculate_result_individual, calculate_result
from competition.serializers import ParticipantSerializer
from django.utils.timezone import now


class ParticipantsViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        return Participant.objects.filter(competition__id=self.kwargs['competition_pk']).all()


class PublicCompetitionViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):

    filter_backends = (SearchFilter,)
    search_fields = ('title',)
    serializer_class = PublicCompetitionSerializer

    def get_queryset(self):
        if self.request.query_params.get('participated'):
            return [p.competition for p in self.request.user.participated.all()]
        return PublicCompetition.objects.filter(finish_time__gte=now()).order_by('start_time').all()

    @action(['GET'], detail=True, url_path='test', url_name='competition_test')
    def test(self, request, pk):
        competition = self.__get_competition(pk)
        participant = competition.participants.filter(user=request.user).first()
        if not participant:
            raise BaseException(detail='Join to competition first', code='not_participant', status=403)
        if participant.end_time:
            raise BaseException(detail='competition finished', code='competition_finished', status=404)

        time = now()
        if competition.start_time > time:
            raise BaseException(detail='competition not started', code='competition_not_started', status=403)
        if competition.finish_time < time:
            raise BaseException(detail='competition finished', code='competition_finished', status=404)

        time_passed = now() - participant.start_time
        if time_passed.seconds >= competition.duration_seconds():
            raise BaseException(detail='competition finished', code='competition_finished', status=404)

        if not participant.start_time:
            participant.start_time = time
            participant.save()
        test_serializer = PublicTestSerializer(instance=competition.test)
        return Response(data=test_serializer.data)

    @action(('POST',), detail=True, url_path='join', url_name='competition_join')
    def join(self, request, pk):
        competition = self.__get_competition(pk)
        if competition.finish_time < now():
            raise BaseException(detail='competition finished', code='competition_finished', status=404)
        participant = Participant.objects.filter(competition=competition, user=request.user).first()
        if not participant:
            Participant.objects.create(competition=competition,
                                       user=request.user,
                                       owner=competition.owner)
        return Response(status=200)

    @action(('POST',), detail=True, url_path='submit', url_name='competition_submit')
    def submission(self, request, pk):
        competition = self.__get_competition(pk)
        participant = self.__get_participant(competition, request)
        submission_serializer = SubmissionSerializer(data=request.data)
        submission_serializer.is_valid(True)
        time_passed = now() - participant.start_time
        if time_passed.seconds >= competition.duration_seconds():
            participant.finish()
            participant.save()
            raise BaseException(detail='competition finished', code='competition_finished', status=404)

        data = submission_serializer.validated_data
        test = competition.test
        question = test.questions.filter(id=data['question'].id).first()
        if not question:
            raise BaseException(detail='question not found', code='not_found', status=404)
        answer = question.answers.filter(id=data['answer'].id).first()
        if not answer:
            raise BaseException(detail='answer not found', code='not_found', status=404)
        submission = Submission.objects.filter(participant=participant, test=test, question=question, answer=answer).first()
        if not submission:
            submission_serializer.save(participant=participant, test=competition.test)
            submission = submission_serializer.instance
        return Response(status=200, data=SubmissionSerializer(instance=submission).data)

    @action(('POST',), detail=True, url_path='delete_submit', url_name='competition_delete_submit')
    def delete_submission(self, request, pk):
        competition = self.__get_competition(pk)
        participant = self.__get_participant(competition, request)
        rm_submission = DeleteSubmissionSerializer(data=request.data)
        rm_submission.is_valid(True)
        submission = Submission.objects.filter(id=rm_submission.data['id'], participant=participant, test=competition.test).first()
        if not competition:
            raise BaseException(status=404, detail='submission not found', code='not_found')
        submission.delete()
        return Response(status=200)

    @action(('POST',), detail=True, url_path='start', url_name='start_test')
    def start_test(self, request, pk):
        competition = self.__get_competition(pk)
        participant = self.__get_participant(competition, request)
        participant.start()
        participant.save()
        s = ParticipantSerializer(instance=participant)
        return Response(s.data)

    @action(('POST',), detail=True, url_path='finish', url_name='finish_test')
    def finish_test(self, request, pk):
        competition = self.__get_competition(pk)
        participant = self.__get_participant(competition, request)
        participant = calculate_result_individual(participant, save=False)
        participant.finish()
        participant.save()
        s = ParticipantSerializer(instance=participant)
        return Response(s.data)

    @action(('GET',), detail=False, url_path='calc_results', url_name='competition_calculate_result')
    def calculate_results(self, request):
        for competition in Competition.objects.all():
            calculate_result(competition)
        return Response(status=200)

    def __get_competition(self, pk):
        competition = self.get_queryset().filter(id=pk).first()
        if not competition:
            raise BaseException(status=404, detail='competition not found', code='not_found')
        return competition

    def __get_participant(self, competition, request):
        participant = Participant.objects.filter(competition=competition, user=request.user).first()
        if not participant:
            raise BaseException(status=403, detail='you are not participant', code='not_participant')
        return participant