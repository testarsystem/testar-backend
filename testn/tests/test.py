from rest_framework.test import APITestCase, APIClient
from testar.test_utils import TestarTest
from testn.models import Test


class TestnTestCase(TestarTest, APITestCase):

    def setUp(self) -> None:
        user = self.create_user("user1", "test1")
        payload, token = user.login()
        self.init_client(token)

    url = '/test/v1/tests/'

    def testSuccessCreateTest(self):
        body = {
            "title": "Final test",
            "description": "The finals"
        }
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 201)

    def testEmptyBody(self):
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 400)

    def testEmptyTitle(self):
        r = self.client.post(self.url, {"description": "the finals"})
        self.assertEqual(r.status_code, 400)

    def testEmptyDescription(self):
        r = self.client.post(self.url, {"title": "Final Test"})
        self.assertEqual(r.status_code, 201)
        self.assertIn('id', r.json())


class TestAccessTestCase(TestarTest, APITestCase):
    _url = '/test/v1/tests/{test_id}/'

    def setUp(self) -> None:
        user1 = self.create_user("user1", "test1")
        user2 = self.create_user("user2", "test2")
        _, token1 = user1.login()
        _, token2 = user2.login()
        self.client1 = self.init_client(token1)
        self.client2 = self.init_client(token2)

        self.test = Test.objects.create(title='Final test', description='the finals', owner=user1)
        self.url = self._url.format(test_id=self.test.id)

    def testSuccessUser(self):
        r = self.client1.get(self.url)
        self.assertEqual(r.status_code, 200)

    def testIncorrectAccess(self):
        r = self.client2.get(self.url)
        self.assertEqual(r.status_code, 404)

    def testWithoutToken(self):
        client = APIClient()
        r = client.get(self.url)
        self.assertEqual(r.status_code, 401)
