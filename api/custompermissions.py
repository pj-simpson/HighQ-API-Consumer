from rest_framework import permissions
from django.contrib.auth.models import Group


class FirstLineOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.groups.filter(name="First Line").exists()
