from django.urls import path
from . import views

app_name = "orgadmin"


urlpatterns = [
    path("search/", views.HighQOrgSearchPage.as_view(), name="org_search"),
    path("submit/", views.HighQOrgSubmitPage.as_view(), name="org_submit"),
    path("search/ajax/org/", views.HighQOrgSearch.as_view(), name="ajax_org_search"),
    path("submit/ajax/org/", views.HighQOrgSubmit.as_view(), name="ajax_org_submit"),
]
