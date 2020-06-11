from django.contrib import admin
from django.urls import path

from . import views

app_name = "useradmin"


urlpatterns = [
    path("search/", views.HighQUserSearchPage.as_view(), name="user_search"),
    path("search/ajax/user/", views.HighQUserSearch.as_view(), name="ajax_user_search"),
    path(
        "search/ajax/remove/", views.HighQUserRemove.as_view(), name="ajax_user_remove"
    ),
    path(
        "search/ajax/reset/",
        views.HighQUserSiteInvite.as_view(),
        name="ajax_user_reset",
    ),
]
