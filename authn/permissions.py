from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return True


class IsAuthenticated(BasePermission):
    ...


