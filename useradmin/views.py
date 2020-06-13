import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from highqsysadmin.settings import base
from siteadmin.token_gen import token_generation
from useradmin.forms import HighQUserForm


# load the index/about page
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        response = render(request, "index.html")
        return response


# load the page where the search form will be


class HighQUserSearchPage(LoginRequiredMixin, View):
    def get(self, request):
        form = HighQUserForm()
        return render(
            request, "useradmin/user_search.html", {"form": form, "nav": "col"}
        )


# view for the ajax call which fetches the search results
class HighQUserSearch(LoginRequiredMixin, View):
    def get(self, request):
        search_result = {}
        if "email" in request.GET:
            form = HighQUserForm(request.GET)
            if form.is_valid():
                search_result = form.search()

        return JsonResponse(search_result)


class HighQUserRemove(LoginRequiredMixin, View):
    def get(self, request):
        result = {}
        token = token_generation()
        user_id = request.GET.get("user_id", "")
        site_id = request.GET.get("site_id", "")
        user_id = int(user_id)
        endpoint = "{instance}api/3/sites/{site_id}/users"
        url = endpoint.format(instance=base.INSTANCE, site_id=site_id)
        headers = {
            "Authorization": "Bearer %s" % token["token_result"]["token"],
            "Content-Type": "application/xml",
            "Accept": "application/json",
        }
        payload = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?><transactionids><transactionid>{user_id}</transactionid></transactionids>""".format(
            user_id=user_id
        )
        response = requests.delete(url, headers=headers, data=payload)

        result = response.json()
        result["success"] = True
        result["message"] = result["transaction"][0]["reason"]
        result["apistatuscode"] = result["transaction"][0]["statuscode"]

        return JsonResponse(result)


# Debug and sort this out first and then copy for suspend:


class HighQUserSiteInvite(LoginRequiredMixin, View):
    def get(self, request):
        result = {}
        token = token_generation()
        user_id = request.GET.get("user_id", "")
        site_id = request.GET.get("site_id", "")
        user_id = int(user_id)
        endpoint = "{instance}api/3/sites/{site_id}/users/invitation"
        url = endpoint.format(instance=base.INSTANCE, site_id=site_id)
        headers = {
            "Authorization": "Bearer %s" % token["token_result"]["token"],
            "Content-Type": "application/xml",
            "Accept": "application/json",
        }
        payload = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?><invitations><messagebody><![CDATA[Site Invite Via HighQ Sys Admin App]]></messagebody><transactionids><transactionid>{user_id}</transactionid></transactionids></invitations>""".format(
            user_id=user_id
        )
        response = requests.put(url, headers=headers, data=payload)

        result = response.json()
        result["success"] = True
        result["message"] = result["transaction"][0]["reason"]
        result["apistatuscode"] = result["transaction"][0]["statuscode"]

        return JsonResponse(result)
