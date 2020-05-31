from django.urls import path

from . import views
app_name = 'tasks'


urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('list/<int:pk>/',views.TaskUserListView.as_view(),name='task_list_user'),
    path('list/unassigned/',views.TaskUnassignedListView.as_view(),name='task_list_unassigned'),
    path('list/complete/',views.TaskCompleteListView.as_view(),name='task_list_complete'),
    path('<int:pk>/<slug:post>/',
         views.TaskDetailView.as_view(),
         name='task_detail'),
    path('create/',views.TaskCreateView.as_view(),
         name='task_create'),
    path('search_results/',views.TaskSearchView.as_view(),
             name='task_search_results'),
    path('edit/<int:pk>/<slug:post>/',
         views.TaskEditView.as_view(),
         name='task_edit'),
    path('push/<int:pk>/<slug:post>/',
         views.TaskPushToCollabView.as_view(),
         name='task_push'),
    path('push/<int:pk>/<slug:post>/ajax/task_list/',
         views.TasksGetSiteTaskList.as_view(), name='ajax_site_task_list'),

]