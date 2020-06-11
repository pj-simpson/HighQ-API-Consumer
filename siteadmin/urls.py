from django.urls import path

from . import views

app_name = "siteadmin"


urlpatterns = [
    path("search/", views.HighQSiteSearchPage.as_view(), name="site_search"),
    path("search/ajax/site/", views.HighQSiteSearch.as_view(), name="ajax_site_search"),
    path(
        "search/ajax/message/",
        views.HighQSiteAdminMessage.as_view(),
        name="ajax_site_message",
    ),
]
