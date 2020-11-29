import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from core.token_gen import token_generation
from useradmin.forms import HighQUserForm


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
        token = token_generation()
        user_id = request.GET.get("user_id", "")
        site_id = request.GET.get("site_id", "")
        user_id = int(user_id)
        url = f"{settings.INSTANCE}api/3/sites/{site_id}/users"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/xml",
            "Accept": "application/json",
        }
        payload = (
            # for some reason this endpoint wasnt accpeting json at the time of coding
            """<?xml version="1.0" encoding="UTF-8" standalone="no" ?><transactionids><transactionid>"""
            f"""{user_id}</transactionid></transactionids>"""
        )
        response = requests.delete(url, headers=headers, data=payload)

        result = response.json()
        result["success"] = True
        result["message"] = result["transaction"][0]["reason"]
        result["apistatuscode"] = result["transaction"][0]["statuscode"]

        return JsonResponse(result)


class HighQUserSiteInvite(LoginRequiredMixin, View):
    def get(self, request):
        token = token_generation()
        user_id = request.GET.get("user_id", "")
        site_id = request.GET.get("site_id", "")
        user_id = int(user_id)
        url = f"{settings.INSTANCE}api/3/sites/{site_id}/users/invitation"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/xml",
            "Accept": "application/json",
        }
        payload = (
            # another endpoint not accpeting json
            """<?xml version="1.0" encoding="UTF-8" standalone="no" ?><invitations><messagebody>"""
            """<![CDATA[Site Invite Via HighQ Sys Admin App]]></messagebody><transactionids>"""
            f"""<transactionid>{user_id}</transactionid></transactionids></invitations>"""
        )
        response = requests.put(url, headers=headers, data=payload)

        result = response.json()
        result["success"] = True
        result["message"] = result["transaction"][0]["reason"]
        result["apistatuscode"] = result["transaction"][0]["statuscode"]

        return JsonResponse(result)
