import json

import requests
from django import forms

from HighQSysAdmProj import settings
from siteadmin.token_gen import token_generation
from siteadmin.forms import is_empty


class HighQOrgSearchForm(forms.Form):
    CHOICES = (('active','active'),('archive','archive'),('pending','pending'))

    orgname = forms.CharField
    domainname = forms.CharField
    status = forms.ChoiceField(choices=CHOICES)

    def search(self):
        token = token_generation()
        result ={}
        orgname = self.data['orgname']
        domainname = self.data['domainname']
        #why are those two fields not in 'cleaned data'?
        status = self.cleaned_data['status']
        endpoint = '{instance}api/4/organisations?search={orgname}&domain={domainname}&status={status}'
        url = endpoint.format(instance=settings.INSTANCE,orgname=orgname,domainname=domainname,status=status)
        headers = {'Authorization':'Bearer %s' % token['token_result']['token'],'Accept':'application/json'}
        response = requests.get(url,headers=headers)

        if response.status_code == 200:
            result = response.json()
            result['success'] = True
            empty_check = result["organisation"]

            if is_empty(empty_check):
                result['message'] = 'No orgs returned for any of the search criteria'
                result['empty_check'] = True
            else:
                result['empty_check'] = False

        else:
            result['success'] = False
            result['message'] = 'The Config of this App or the API it consumes, currently has an issue.'

        return result


class HighQOrgSubmitForm(forms.Form):
    CHOICES = (('active','active'),('archive','archive'),('pending','pending'))

    orgname = forms.CharField
    url = forms.URLField
    status = forms.ChoiceField(choices=CHOICES)

    def submit(self):
        token = token_generation()
        result ={}
        orgname = self.data['orgname']
        orgurl = self.data['orgurl']
        #why are those two fields not in 'cleaned data'?
        status = self.cleaned_data['status']
        endpoint = '{instance}api/4/organisations'
        url = endpoint.format(instance=settings.INSTANCE)
        headers = {'Authorization':'Bearer %s' % token['token_result']['token'],'Accept':'application/json','Content-Type': 'application/json'}
        payload = json.dumps({"name": orgname,"status": status,"url": orgurl}) #we are using dumps here because endpoint only accepts strings in json in double quotes
        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            result['success'] = True
            result['message'] = 'New Org Created'
        else:
            result['success'] = False
            result['message'] =  'Failed to create an Org'

        return result





