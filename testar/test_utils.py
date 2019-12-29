from authn.models import User
from rest_framework.test import APIClient


class TestarTest:
    client = None

    def init_client(self, token=None):
        self.client = APIClient(HTTP_AUTHORIZATION=token)
        return self.client

    @staticmethod
    def create_user(username, password):
        user = User(name=username, username=username)
        user.set_password(password)
        user.save()
        return user
