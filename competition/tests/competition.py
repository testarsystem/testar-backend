from rest_framework.test import APITestCase
from testar.test_utils import TestarTest
from testn.models import Test


class CompetitionTestCase(TestarTest, APITestCase):
    url = '/competition/v1/competitions/'

    @staticmethod
    def __create_body(**kwargs):
        return {**kwargs}

    def setUp(self) -> None:
        user = self.create_user('user1', 'test1')
        _, token = user.login()
        self.init_client(token)
        self.test = Test.objects.create(title='Final test', description='the finals', owner=user)

    def testSuccess(self):
        body = self.__create_body(title='Competition1',
                                  start_time='2019-12-10T06:33:00.000Z',
                                  finish_time='2019-12-13T05:33:00.000Z',
                                  duration="1:00",
                                  test=self.test.id)
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 201)

    def testIncorrectTest(self):
        body = self.__create_body(title='Competition1',
                                  start_time='2019-12-10T06:33:00.000Z',
                                  finish_time='2019-12-13T05:33:00.000Z',
                                  duration="1:00",
                                  test=2)
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 400)

    def testEmtyBody(self):
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 400)

    def testFinishTimeLowerThanStartTime(self):
        body = self.__create_body(title='Competition1',
                                  start_time='2019-12-10T06:33:00.000Z',
                                  finish_time='2018-12-13T05:33:00.000Z',
                                  duration="1:00",
                                  test=self.test.id)
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 400)

    def testWrongDurationFormat(self):
        body = self.__create_body(title='Competition1',
                                  start_time='2019-12-10T06:33:00.000Z',
                                  finish_time='2019-12-13T05:33:00.000Z',
                                  duration="0",
                                  test=self.test.id)
        r = self.client.post(self.url, body)
        self.assertEqual(r.status_code, 400)
