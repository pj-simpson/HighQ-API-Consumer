from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import get_object_or_404

from tasks.models import Task


class Action(models.Model):
    user = models.ForeignKey(
        "auth.User", related_name="actions", on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_ct", "target_id")

    class Meta:
        ordering = ("-created",)

    def get_task_url(self):
        task = get_object_or_404(Task, pk=self.target_id)
        return task.get_absolute_url()
