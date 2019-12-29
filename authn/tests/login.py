from django.test import TestCase, Client
from testar.test_utils import TestarTest


class LoginTestCase(TestarTest, TestCase):

    def setUp(self):
        self.create_user("user1", 'test1')
        self.create_user("user2", 'test2')

    def testSuccessLogin(self):
        c = Client()
        response = c.post('/auth/v1/login/', {'testar': 'user1', 'password': 'test1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def testIncorrectPassLogin(self):
        c = Client()
        response = c.post('/auth/v1/login/', {'testar': 'user1', 'password': '123456'})
        self.assertEqual(response.status_code, 401)



