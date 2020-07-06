import requests

from highqsysadmin.settings import base
from core.token_gen import token_generation


def get_task_status(site_id):

    token = token_generation()
    result = {}
    siteid = site_id
    endpoint = "{instance}api/3/tasks/status?siteid={siteid}"
    url = endpoint.format(instance=base.INSTANCE, siteid=siteid)
    headers = {
        "Authorization": "Bearer %s" % token["token_result"]["token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        status = result["status"][0]["statusid"]
        return status
    else:
        return siteid
