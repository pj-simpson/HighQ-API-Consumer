from django import forms
from django.conf import settings
import requests
from django.http import JsonResponse
from .token_gen import token_generation

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


class HighQSiteForm(forms.Form):
    sitename = forms.CharField()

    def search(self):
        token = token_generation()
        result ={}
        sitename = self.cleaned_data['sitename']
        endpoint = '{instance}api/6/sites/?name={sitename}'
        url = endpoint.format(instance=settings.INSTANCE,sitename=sitename)
        headers = {'Authorization':'Bearer %s' % token['token_result']['token'],'Accept':'application/json'}
        response = requests.get(url,headers=headers)


        if response.status_code == 200:
            result = response.json()
            result['success'] = True
            empty_check = result["site"]

            # calculate the percentage of the site size taken up by deleted items
            for i in result['site']:
                if i['rawsitesize']['totalsize'] > 0:
                    deleteddoc = i['rawsitesize']['deleteddocumentsize']
                    total = i['rawsitesize']['totalsize']
                    # work out how to deal with 0 division.
                    percentage_deleted = (deleteddoc/total)* 100
                    percentage_deleted = round(percentage_deleted,2)
                    i['percentage_deleted'] = percentage_deleted
                else:
                    i['percentage_deleted'] = 0.00

            if is_empty(empty_check):
                result['message'] = 'No sites returned for %s' % sitename
                result['empty_check'] = True
            else:
                result['empty_check'] = False

        else:
            result['success'] = False
            result['message'] = 'The Config of this App or the API it consumes, currently has an issue.'

        return result


class HighQSiteOwnerMessage(forms.Form):
    email_message = forms.CharField()
    user_id = forms.IntegerField()
    site_id = forms.IntegerField()

    def send(self):
        token = token_generation()
        result ={}
        email_message = self.cleaned_data['email_message']
        user_id = self.cleaned_data['user_id']
        site_id = self.cleaned_data['site_id']
        endpoint = '{instance}api/3/sites/{site_id}/users/email'
        url = endpoint.format(instance=settings.INSTANCE,site_id=site_id)
        headers = {'Authorization':'Bearer %s' % token['token_result']['token'],'Content-Type': 'application/xml','Accept': 'application/json'}
        payload = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?><emailusers><emailsubject>Message From HighQ Sys Admin App</emailsubject><messagebody><![CDATA[{email_message}]]></messagebody><transactionids><transactionid>{user_id}</transactionid></transactionids></emailusers>""".format(user_id=user_id ,email_message=email_message)
        response = requests.put(url, headers=headers, data=payload)

        result = response.json()
        result['success'] = True
        result['message'] = result['transaction'][0]['reason']
        result['apistatuscode'] = result['transaction'][0]['statuscode']

        return result

