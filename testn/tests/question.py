from rest_framework.test import APITestCase
from testar.test_utils import TestarTest
from testn.models import Test


class QuestionTestCase(TestarTest, APITestCase):
    _url = '/test/v1/tests/{test_id}/questions/'

    def setUp(self) -> None:
        user = self.create_user("user1", "test1")
        payload, token = user.login()
        self.init_client(token)
        test = Test.objects.create(title='Final test', description='the finals', owner=user)
        self.url = self._url.format(test_id=test.id)

    def testSuccessCreateQuestion(self):
        body = {
            "text": "2 + 2"
        }
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 201)

    def testEmptyBody(self):
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 400)

    def testIncorrectTestId(self):
        body = {
            "text": "2 + 2"
        }
        r = self.client.post(self._url.format(test_id=2), body)
        self.assertEqual(r.status_code, 404)

