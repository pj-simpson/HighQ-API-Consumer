import requests
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from HighQSysAdmProj.settings import base


from siteadmin.token_gen import token_generation
from .models import Task
from .forms import TaskCollabPushForm
from .get_task_statuses import get_task_status


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

class TaskPushSuccessView(View):

    @method_decorator(login_required)
    def get(self,request,pk,post):
        task = get_object_or_404(Task,pk=pk)
        return render(request,'tasks/task_push_success.html',{'task':task})

class TaskPushFailureView(View):

    @method_decorator(login_required)
    def get(self,request,pk,post):
        task = get_object_or_404(Task,pk=pk)
        return render(request,'tasks/task_push_fail.html',{'task':task})

class TaskPushToCollabView(View):

    @method_decorator(login_required)
    def get(self, request,pk,post):
        form = TaskCollabPushForm()
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/task_push_form.html',{'form': form})

    @method_decorator(login_required)
    def post(self, request, pk, post):

        task = get_object_or_404(Task,pk=pk)

        form = TaskCollabPushForm(request.POST)
        if form:

            result = {}
            task_list_id = form.data['task_list']
            site_id = form.data['site']
            endpoint = '{instance}api/3/tasks?tasklistid={tasklistid}'
            url = endpoint.format(instance=base.INSTANCE,tasklistid=task_list_id)

            payload = json.dumps({"title": task.subject,
                                    "description": task.body,
                                  "priority":{"priorityid":1},
                                  "status":{"statusid":get_task_status(site_id)},
                                    "startdate": task.created.__str__(),
                                    "tags": {"tag": [{"tagname": "Pushed From HighQSysAdminApp"}]}})
            # create the token later
            token = token_generation()
            headers = {'Authorization': 'Bearer %s' % token['token_result']['token'], 'Accept': 'application/json',
                       'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=payload)

            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                task.ispushed = True
                task.save()
                return redirect('tasks:task_push_success',pk=task.pk,post=task.slug)
            else:
                return redirect('tasks:task_push_failure', pk=task.pk, post=task.slug)





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


