from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import render
from django.views.generic import ListView

from .models import Action


class ActionListView(ListView, LoginRequiredMixin):
    model = Action
    paginate_by = 6
    context_object_name = "actions"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs.exclude(user=self.request.user)
            .select_related("user")
            .prefetch_related("target_ct")
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav"] = "activity"
        return context
