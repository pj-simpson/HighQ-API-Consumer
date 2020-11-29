import json

import requests
from django import forms
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from core.token_gen import token_generation
from siteadmin.forms import is_empty


class HighQOrgSearchForm(forms.Form):
    CHOICES = (("active", "active"), ("archive", "archive"), ("pending", "pending"))

    orgname = forms.CharField
    domainname = forms.CharField
    status = forms.ChoiceField(choices=CHOICES)

    def search(self):
        token = token_generation()
        try:
            orgname = self.data["orgname"]
        except MultiValueDictKeyError:
            orgname = None
        try:
            domainname = self.data["domainname"]
        except MultiValueDictKeyError:
            domainname = None
            pass
        # why are those two fields not in 'cleaned data'?
        status = self.cleaned_data["status"]
        if not orgname:
            url = f"{settings.INSTANCE}api/4/organisations?domain={domainname}&status={status}"
        elif not domainname:
            url = f"{settings.INSTANCE}api/4/organisations?searchTxt={orgname}&status={status}"
        else:
            url = f"{settings.INSTANCE}api/4/organisations?searchTxt={orgname}&domain={domainname}&status={status}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()
            result["success"] = True
            empty_check = result["organisation"]

            if is_empty(empty_check):
                result["message"] = "No orgs returned for any of the search criteria"
                result["empty_check"] = True
            else:
                result["empty_check"] = False

        else:
            result = {}
            result["success"] = False
            result[
                "message"
            ] = "The Config of this App or the API it consumes, currently has an issue."

        return result


class HighQOrgSubmitForm(forms.Form):
    CHOICES = (("active", "active"), ("archive", "archive"), ("pending", "pending"))

    orgname = forms.CharField
    url = forms.URLField
    domain = forms.CharField
    status = forms.ChoiceField(choices=CHOICES)

    def submit(self):
        token = token_generation()
        orgname = self.data["orgname"]
        orgurl = self.data["orgurl"]
        # why are those two fields not in 'cleaned data'?
        status = self.cleaned_data["status"]
        domain = self.data["orgdomain"]
        url = f"{settings.INSTANCE}api/4/organisations"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = json.dumps(
            {"name": orgname, "status": status, "url": orgurl}
        )  # we are using dumps here because endpoint only accepts strings in json in double quotes
        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            result["success"] = True
            result["message"] = "New Org Created"

            orgid = result["orgid"]
            url = f"{settings.INSTANCE}api/4/domains?orgid={orgid}"
            token2 = token_generation()
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            payload = json.dumps({"url": domain, "status": "active"})
            response = requests.post(url, headers=headers, data=payload)

            if response.status_code == 200 or response.status_code == 201:
                result["domainresult"] = response.json()
                result["message"] = "New Org And Domain Created"

            else:
                result["success"] = False
                result["message"] = "Created the domain but failed to create an org"

        else:
            result = {}
            result["success"] = False
            result["message"] = "Failed to create an Org"

        return result
