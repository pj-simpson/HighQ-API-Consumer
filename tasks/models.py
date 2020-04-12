from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):

    class Status(models.TextChoices):
        NEW = 'new',"New"
        IN_PROG = 'in_progress',"In Progress"
        COMP = 'complete',"Complete"

    subject = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='created')
    poster = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='tasks_posted')
    asignee = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='tasks_assigned', null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12,choices=Status.choices,
                              default=Status.NEW)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject)
        super(Task, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tasks:task_detail',
                       args=[self.pk,
                             self.slug])

    def get_possible_assignees(self):
        return User.objects.get_queryset().filter(groups__name='Second Line')
