from django.urls import path

from . import views

app_name = "profiles"


urlpatterns = [
    path("<int:pk>/", views.DetailProfileView.as_view(), name="profile_detail"),
    path("edit/", views.EditProfileView.as_view(), name="edit_profile"),
]
