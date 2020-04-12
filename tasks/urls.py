from django.urls import path
from . import views
app_name = 'tasks'


urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('list/<int:pk>/',views.TaskUserListView.as_view(),name='task_list_user'),
    path('list/unassigned/',views.TaskUnassignedListView.as_view(),name='task_list_unassigned'),
    path('<int:pk>/<slug:post>/',
         views.TaskDetailView.as_view(),
         name='task_detail'),
    path('create/',views.TaskCreateView.as_view(),
         name='task_create'),
    path('edit/<int:pk>/<slug:post>/',
         views.TaskEditView.as_view(),
         name='task_edit'),

]