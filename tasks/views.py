from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from .models import Task


class TaskCreateView(CreateView,PermissionRequiredMixin):
    model = Task
    fields = ['subject','body']
    template_name_suffix ='_create_form'

    def form_valid(self,form):
        form.instance.poster = self.request.user
        super(TaskCreateView, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class TaskListView(ListView, PermissionRequiredMixin):
    model = Task

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(asignee=self.request.user)|Q(asignee__isnull=True)).exclude(status='complete')

class TaskUnassignedListView(TaskListView,PermissionRequiredMixin):

    def get_queryset(self):
        return self.model.objects.filter(asignee__isnull=True).exclude(status='complete')

class TaskUserListView(TaskListView,PermissionRequiredMixin):
    def get_queryset(self):
        return self.model.objects.filter(asignee__id=self.kwargs['pk']).exclude(status='complete')

class TaskCompleteListView(TaskListView,PermissionRequiredMixin):
    def get_queryset(self):
        return self.model.objects.filter(status='complete')


class TaskDetailView(DetailView,PermissionRequiredMixin):
    model = Task

class TaskEditView(UpdateView,PermissionRequiredMixin):
    model = Task
    fields = ['status', 'asignee']
    success_url = '/tasks/'

