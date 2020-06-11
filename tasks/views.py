import json

import requests
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from actions.utils import create_action
from HighQSysAdmProj.settings import base
from siteadmin.token_gen import token_generation

from .forms import TaskCollabPushForm
from .get_task_statuses import get_task_status
from .models import Task


class TaskCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView, SuccessMessageMixin
):
    model = Task
    fields = ["subject", "body"]
    template_name_suffix = "_create_form"
    success_message = "Task Successfully created!"
    permission_required = "tasks.add_task"
    context_object_name = "task"

    def form_valid(self, form):
        form.instance.poster = self.request.user
        super(TaskCreateView, self).form_valid(form)
        create_action(self.request.user, "just raised a new issue:", self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "tasks"
        context["menu"] = "create"
        return context


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            Q(asignee=self.request.user) | Q(asignee__isnull=True)
        ).exclude(status="complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "tasks"
        context["menu"] = "list"
        return context


class TaskUnassignedListView(TaskListView):
    def get_queryset(self):
        return self.model.objects.filter(asignee__isnull=True).exclude(
            status="complete"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "tasks"
        context["menu"] = "unassigned"
        return context


class TaskUserListView(TaskListView):
    def get_queryset(self):
        return self.model.objects.filter(asignee__id=self.kwargs["pk"]).exclude(
            status="complete"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "tasks"
        context["menu"] = "me"
        return context


class TaskCompleteListView(TaskListView):
    def get_queryset(self):
        return self.model.objects.filter(status="complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "tasks"
        context["menu"] = "complete"
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "tasks"
        return context


class TaskEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    fields = ["status", "asignee"]
    success_url = "/tasks/"
    success_message = "Task Successfully updated!"
    permission_required = "tasks.change_task"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "tasks"
        return context

    def form_valid(self, form):
        super(TaskEditView, self).form_valid(form)
        create_action(self.request.user, "just updated an issue:", self.object)
        return HttpResponseRedirect(self.get_success_url())


class TaskPushToCollabView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "tasks.change_task"

    def get(self, request, pk, post):
        form = TaskCollabPushForm()
        task = get_object_or_404(Task, pk=pk)
        return render(
            request, "tasks/task_push_form.html", {"form": form, "nav": "tasks"}
        )

    def post(self, request, pk, post):

        task = get_object_or_404(Task, pk=pk)
        form = TaskCollabPushForm(request.POST)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["nav"] = "tasks"
            return context

        if form:

            result = {}
            task_list_id = form.data["task_list"]
            site_id = form.data["site"]
            endpoint = "{instance}api/3/tasks?tasklistid={tasklistid}"
            url = endpoint.format(instance=base.INSTANCE, tasklistid=task_list_id)

            payload = json.dumps(
                {
                    "title": task.subject,
                    "description": task.body,
                    "priority": {"priorityid": 1},
                    "status": {"statusid": get_task_status(site_id)},
                    "startdate": task.created.__str__(),
                    "tags": {"tag": [{"tagname": "Pushed From HighQSysAdminApp"}]},
                }
            )
            # we create the token later
            token = token_generation()
            headers = {
                "Authorization": "Bearer %s" % token["token_result"]["token"],
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            response = requests.post(url, headers=headers, data=payload)

            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                task.ispushed = True
                task.save()
                create_action(request.user, "just pushed a task to collaborate:", task)
                messages.success(request, "Task Successfully Pushed To Collaborate")
                return redirect("tasks:task_list")
            else:
                messages.error(request, "Task Successfully Pushed To Collaborate")
                return redirect("tasks:task_list")


class TasksGetSiteTaskList(LoginRequiredMixin, View):
    def get(self, request, pk, post):
        token = token_generation()
        result = {}
        site_id = request.GET.get("siteid", "")
        endpoint = "{instance}api/3/tasks/lists?siteid={site_id}"
        url = endpoint.format(instance=base.INSTANCE, site_id=site_id)
        headers = {
            "Authorization": "Bearer %s" % token["token_result"]["token"],
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return JsonResponse(result)


class TaskSearchView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/search_results.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        return Task.objects.filter(
            Q(subject__icontains=query) | Q(body__icontains=query)
        )
