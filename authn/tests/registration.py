from django.test import TestCase, Client
from authn.models import User
from testar.test_utils import TestarTest


class RegistrationTestCase(TestarTest, TestCase):

    @staticmethod
    def __create_body(username, password):
        return {"username": username, "password": password}

    url = '/auth/v1/registration/'

    def setUp(self):
        self.create_user("user1", 'test1')

    def testSuccessRegistration(self):
        c = Client()
        response = c.post(self.url, self.__create_body("user2", "test2"))
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.json())

    def testUniqueUsername(self):
        c = Client()
        response = c.post(self.url, self.__create_body("user1", "test1"))
        self.assertEqual(response.status_code, 400)



