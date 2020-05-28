from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from orgadmin.forms import HighQOrgSearchForm, HighQOrgSubmitForm


class HighQOrgSearchPage(LoginRequiredMixin,View):

    def get(self, request):
        form = HighQOrgSearchForm()
        return render(request, 'orgadmin/orgsearch.html', {'form': form, 'nav':'col'})

class HighQOrgSearch(LoginRequiredMixin,View):

    def get(self, request):
        search_result = {}
        if 'orgname' in request.GET or 'domainname' in request.GET:
            form = HighQOrgSearchForm(request.GET)
            if form.is_valid():
                search_result = form.search()

        return JsonResponse(search_result,safe=False)


class HighQOrgSubmitPage(LoginRequiredMixin,View):

    def get(self, request):
        form = HighQOrgSubmitForm()
        return render(request, 'orgadmin/orgsubmit.html', {'form': form, 'nav':'col'})

class HighQOrgSubmit(LoginRequiredMixin,View):

    def get(self, request):
        search_result = {}
        if 'orgname' in request.GET:
            form = HighQOrgSubmitForm(request.GET)
            if form.is_valid():
                search_result = form.submit()

        return JsonResponse(search_result,safe=False)