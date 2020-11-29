import requests
from django.conf import settings

from core.token_gen import token_generation


def get_task_status(site_id):

    token = token_generation()
    siteid = site_id
    url = f"{settings.INSTANCE}api/3/tasks/status?siteid={siteid}"
    headers = {
        "Authorization": f"Bearer {token}",
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
