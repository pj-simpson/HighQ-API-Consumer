import requests
from django import forms
from django.conf import settings

from core.token_gen import token_generation


class HighQUserForm(forms.Form):
    email = forms.EmailField(max_length=200)

    def search(self):
        result = {}
        token = token_generation()
        email = self.cleaned_data["email"]
        endpoint = "{instance}api/6/users/{user_email}?type=email"
        url = endpoint.format(instance=settings.INSTANCE, user_email=email)
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()
            result["success"] = True

        if response.status_code == 403:
            result = response.json()
            result["success"] = False

        return result
