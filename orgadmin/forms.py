import json

import requests
from django import forms

from HighQSysAdmProj.settings import base
from siteadmin.forms import is_empty
from siteadmin.token_gen import token_generation


class HighQOrgSearchForm(forms.Form):
    CHOICES = (("active", "active"), ("archive", "archive"), ("pending", "pending"))

    orgname = forms.CharField
    domainname = forms.CharField
    status = forms.ChoiceField(choices=CHOICES)

    def search(self):
        token = token_generation()
        result = {}
        try:
            orgname = self.data["orgname"]
        except:
            orgname = None
            pass
        try:
            domainname = self.data["domainname"]
        except:
            domainname = None
            pass
        # why are those two fields not in 'cleaned data'?
        status = self.cleaned_data["status"]
        endpoint = ""
        if not orgname:
            endpoint = (
                "{instance}api/4/organisations?domain={domainname}&status={status}"
            )
        elif not domainname:
            endpoint = (
                "{instance}api/4/organisations?searchTxt={orgname}&status={status}"
            )
        else:
            endpoint = "{instance}api/4/organisations?searchTxt={orgname}&domain={domainname}&status={status}"

        url = endpoint.format(
            instance=base.INSTANCE,
            orgname=orgname,
            domainname=domainname,
            status=status,
        )
        headers = {
            "Authorization": "Bearer %s" % token["token_result"]["token"],
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
        result = {}
        orgname = self.data["orgname"]
        orgurl = self.data["orgurl"]
        # why are those two fields not in 'cleaned data'?
        status = self.cleaned_data["status"]
        domain = self.data["orgdomain"]
        endpoint = "{instance}api/4/organisations"
        url = endpoint.format(instance=base.INSTANCE)
        headers = {
            "Authorization": "Bearer %s" % token["token_result"]["token"],
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
            endpoint = "{instance}api/4/domains?orgid={orgid}"
            url = endpoint.format(instance=base.INSTANCE, orgid=orgid)
            token2 = token_generation()
            headers = {
                "Authorization": "Bearer %s" % token2["token_result"]["token"],
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
            result["success"] = False
            result["message"] = "Failed to create an Org"

        return result
