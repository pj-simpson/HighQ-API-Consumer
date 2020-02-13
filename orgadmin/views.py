from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from orgadmin.forms import HighQOrgSearchForm, HighQOrgSubmitForm


class HighQOrgSearchPage(View):
    @method_decorator(login_required)
    def get(self, request):
        form = HighQOrgSearchForm()
        return render(request, 'orgadmin/orgsearch.html', {'form': form})

class HighQOrgSearch(View):
    @method_decorator(login_required)
    def get(self, request):
        search_result = {}
        if 'orgname' in request.GET:
            form = HighQOrgSearchForm(request.GET)
            if form.is_valid():
                search_result = form.search()

        return JsonResponse(search_result,safe=False)


class HighQOrgSubmitPage(View):
    @method_decorator(login_required)
    def get(self, request):
        form = HighQOrgSubmitForm()
        return render(request, 'orgadmin/orgsubmit.html', {'form': form})

class HighQOrgSubmit(View):
    @method_decorator(login_required)
    def get(self, request):
        search_result = {}
        if 'orgname' in request.GET:
            form = HighQOrgSubmitForm(request.GET)
            if form.is_valid():
                search_result = form.submit()

        return JsonResponse(search_result,safe=False)