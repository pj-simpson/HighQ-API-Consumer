from rest_framework import generics,filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.filters import OrderingFilter,SearchFilter
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
    ordering=['id']
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    ordering_fields = ('id',)
    search_fields =('^username','^first_name','^last_name','^email')

class UserDetailEndpoint(RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class TaskListEndpoint(ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated,FirstLineOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    name = 'task-list'
    ordering = ['created']
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    ordering_fields = ('created',)
    search_fields = ('^body', '^subject',)
    filter_fields = ('poster','asignee','status','ispushed',)

class TaskDetailEndpoint(RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    name = 'task-detail'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'users': reverse('api:user-list',request=request),
            'tasks': reverse('api:task-list',request=request),
        })


