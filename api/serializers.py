from rest_framework import serializers
from tasks.views import Task
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name')


class TaskSerializer(serializers.ModelSerializer):

    asignee = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')
    poster = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')

    class Meta:
        model = Task
        fields = ('id',
                  'subject',
                  'poster',
                  'asignee',
                  'body',
                  'created',
                  'updated',
                  'status',
                  'ispushed',
                  )

