from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from authn.jwt_utils import generate_token

class UserManager(BaseUserManager):
    def _create_user(self, commit=True, **kwargs):
        password = kwargs.pop('password')
        user = self.model(**kwargs)
        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user

    def create_superuser(self, password, username):
        user = self._create_user(password=password, username=username)
        user.is_superuser = True
        user.save()
        return user

    def create_user(self, commit=True, **kwargs):
        return self._create_user(commit, **kwargs)


class User(AbstractBaseUser):
    class Meta:
        db_table = 'user'

    objects = UserManager()
    USERNAME_FIELD = 'username'

    name = models.CharField('name', max_length=50, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)

    is_active = models.BooleanField('is active', default=True)
    is_superuser = models.BooleanField('is superuser', default=False)

    def __str__(self):
        return f'{self.name}'

    @property
    def is_staff(self):
        return self.is_superuser

    def has_module_perms(self, *args, **kwargs):
        return self.is_superuser

    def has_perm(self, *args, **kwargs):
        return self.is_superuser

    def login(self, payload=None):
        if not payload:
            payload = {}
        payload_data = {
            "id": self.id,
            **payload
        }
        return payload_data, generate_token(payload_data)

