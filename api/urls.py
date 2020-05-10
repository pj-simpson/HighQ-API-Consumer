from django.urls import path

from . import views


app_name = 'api'


urlpatterns = [
    path('users/', views.UserListEndpoint.as_view(), name=views.UserListEndpoint.name),
    path('user/<int:pk>',views.UserDetailEndpoint.as_view(),name=views.UserDetailEndpoint.name),
    path('tasks/', views.TaskListEndpoint.as_view(), name=views.TaskListEndpoint.name),
    path('task/<int:pk>',views.TaskDetailEndpoint.as_view(),name=views.TaskDetailEndpoint.name),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),

]