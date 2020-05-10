from rest_framework import generics,filters
from django_filters import AllValuesFilter,DateTimeFilter,NumberFilter

from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .custompermissions import FirstLineOrReadOnly

from tasks.models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.models import User



class UserListEndpoint(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    ordering_fields = ('id',)
    search_fields =('^username','^first_name','^last_name','^email')

class UserDetailEndpoint(RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    filter_backends = None


class TaskListEndpoint(ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated,FirstLineOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    name = 'task-list'
    ordering = ['created']
    ordering_fields = ('created',)
    search_fields = ('^body', '^subject',)
    filter_fields = ('poster','asignee','status','ispushed',)

class TaskDetailEndpoint(RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    name = 'task-detail'
    filter_backends = None

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    filter_backends = None
    def get(self, request, *args, **kwargs):
        return Response({
            'users': reverse('api:user-list',request=request),
            'tasks': reverse('api:task-list',request=request),
        })


