"""HighQSysAdmProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from useradmin import views
from profiles.views import UserRegisterView

from django.views.generic import RedirectView


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', include('useradmin.urls')),
    path('sites/', include('siteadmin.urls')),
    path('orgs/', include('orgadmin.urls')),
    path('profile/', include('profiles.urls')),
    path('tasks/', include('tasks.urls')),
    path('activity/', include('actions.urls')),
    path('admin/', admin.site.urls),
    path('register/',UserRegisterView.as_view(),name='register'),
    path('accounts/register/', RedirectView.as_view(pattern_name='register', permanent=True)),
    path('accounts/', include('registration.backends.simple.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include('api.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

