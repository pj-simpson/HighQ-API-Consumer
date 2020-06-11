from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.views import Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {"url": {"view_name": "api:user-detail"}}
        fields = ("id", "username", "first_name", "last_name", "email", "url")


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    asignee = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )
    poster = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = Task
        extra_kwargs = {"url": {"view_name": "api:task-detail"}}
        fields = (
            "id",
            "subject",
            "body",
            "poster",
            "asignee",
            "created",
            "updated",
            "status",
            "ispushed",
            "url",
        )
