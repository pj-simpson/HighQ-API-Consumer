import requests
from django import forms
from siteadmin.token_gen import token_generation
from HighQSysAdmProj.settings import base


def get_sites_with_tasks():
    token = token_generation()
    result = {}
    endpoint = '{instance}api/4/sites?'
    url = endpoint.format(instance=base.INSTANCE)
    headers = {'Authorization': 'Bearer %s' % token['token_result']['token'], 'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        # make result a list of dicts
        result = result['site']
        list = [("", "")]
        for i in result:
            if i['module']['task']['enable'] == '1':
                list.append((i['id'], i['sitename']))
        return list



class TaskCollabPushForm(forms.Form):

    initial_tasks = (("",""),("",""))
    site = forms.ChoiceField(choices=tuple(get_sites_with_tasks()))
    task_list = forms.ChoiceField(choices=initial_tasks)



