from rest_framework.test import APITestCase
from testar.test_utils import TestarTest
from testn.models import Test, Question


class AnswerTestCase(TestarTest, APITestCase):
    _url = '/test/v1/tests/{test_id}/questions/{question_id}/answers/'

    def setUp(self) -> None:
        user = self.create_user("user1", "test1")
        payload, token = user.login()
        self.init_client(token)
        self.test = Test.objects.create(title='Final test', description='the finals', owner=user)
        self.question = Question.objects.create(text="2 + 2", test=self.test, owner=user)
        self.url = self._url.format(test_id=self.test.id, question_id=self.question.id)

    def testSuccessCreateAnswer(self):
        body = {
            "text": "4",
            "correct": True
        }
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 201)

    def testSecondSuccessCreateAnswer(self):
        body = {
            "text": "5",
            "correct": False
        }
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 201)

    def testEmptyBody(self):

        r = self.client.post(self.url)

        self.assertEqual(r.status_code, 400)

    def testIncorrectTestId(self):
        body = {
            "text": "5",
            "correct": False
        }
        r = self.client.post(self._url.format(test_id=2, question_id=self.question.id), body)
        self.assertEqual(r.status_code, 404)

    def testIncorrectQuestionId(self):
        body = {
            "text": "5",
            "correct": False
        }
        r = self.client.post(self._url.format(test_id=self.test.id, question_id=2), body)
        self.assertEqual(r.status_code, 404)

