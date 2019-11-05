from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend as BaseModelBackend
from django.db.models import Q


UserModel = get_user_model()


class ModelBackend(BaseModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            return None
        try:
            user = UserModel.objects.get(Q(username=username))
        except UserModel.DoesNotExist:
            pass
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active or not user_obj.is_superuser:
            return False
        return True

    def has_module_perms(self, user_obj, app_label):
        if not user_obj.is_active or not user_obj.is_superuser:
            return False
        return True
