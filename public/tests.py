from rest_framework.test import APITestCase
from testar.test_utils import TestarTest
from testn.models import Test, Question, Answer
from competition.models import Competition, Participant


class CompetitionTestCase(TestarTest, APITestCase):
    _url = '/public/v1/competitions/{competition_id}/submit/'

    @staticmethod
    def __create_body(**kwargs):
        return {**kwargs}

    def setUp(self) -> None:
        user = self.create_user('user1', 'test1')
        _, token = user.login()
        self.init_client(token)
        self.test = Test.objects.create(title='Final test', description='the finals', owner=user)
        self.question = Question.objects.create(text="2 + 2", test=self.test, owner=user)
        self.correctAnswer = Answer.objects.create(text='4', correct=True, question=self.question, owner=user)
        self.incorrectAnswer = Answer.objects.create(text='5', correct=False, question=self.question, owner=user)

        self.competition = Competition.objects.create(title='a',
                                                      test=self.test,
                                                      start_time='2019-12-10T06:33:00.000Z',
                                                      finish_time='2020-12-13T05:33:00.000Z',
                                                      duration="1:00",
                                                      owner=user)
        p = Participant(competition=self.competition, user=user, owner=user)
        p.start()
        p.save()
        self.url = self._url.format(competition_id=self.competition.id)

    def testSuccess(self):
        body = self.__create_body(question=self.question.id, answer=self.correctAnswer.id)
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 200)

    def testIncorrectCompetition(self):
        body = self.__create_body(question=self.question.id, answer=self.correctAnswer.id)
        r = self.client.post(self._url.format(competition_id=2), body)
        self.assertEqual(r.status_code, 404)

    def testIncorrectQuestion(self):
        body = self.__create_body(question=self.question.id, answer=self.correctAnswer.id)
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 200)

    def testIncorrectAnswer(self):
        body = self.__create_body(question=self.question.id, answer=3)
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 400)



