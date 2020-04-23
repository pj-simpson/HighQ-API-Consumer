import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from HighQSysAdmProj.settings import base


from siteadmin.token_gen import token_generation
from .models import Task
from .forms import TaskCollabPushForm


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

class TaskPushToCollabView(View):

    @method_decorator(login_required)
    def get(self, request,pk,post):
        form = TaskCollabPushForm()
        return render(request, 'tasks/task_push_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request, pk, post):
        form = TaskCollabPushForm()
        return render(request, 'tasks/task_push_form.html', {'form': form})

class TasksGetSiteTaskList(View):

    @method_decorator(login_required)
    def get(self, request,pk,post):
        token = token_generation()
        result = {}
        site_id = request.GET.get('siteid', '')
        endpoint = '{instance}api/3/tasks/lists?siteid={site_id}'
        url = endpoint.format(instance=base.INSTANCE,site_id=site_id)
        headers = {'Authorization': 'Bearer %s' % token['token_result']['token'], 'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return JsonResponse(result)
