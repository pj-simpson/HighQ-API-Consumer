from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone

from .models import OauthToken


# helper function -- is a datetime within 30 mins of now?
def is_close(a_datetime):
    if ((a_datetime - timezone.now()).total_seconds() / 1800) <= 15:
        return True
    else:
        return False


def token_generation():
    check = OauthToken.objects.filter(gen_time__lte=timezone.now()).count()
    # If there are no OauthToken records in the DB, we use the initial token function.
    if check == 0:
        result = initial_token()

    # If there is at least one record in the DB, we grab the latest and check if it expires soon. If not we use it
    # If it does expire soon (or is in the past) , we call the refresh_token function. The refresh token always expries
    # one year in the future

    if check > 0:
        latest_token = OauthToken.objects.latest("gen_time")
        if not is_close(latest_token.access_token_expires):
            result = latest_token.access_token
        else:
            result = refresh_token(latest_token)

    return result


def save_token_details_and_return(token_response):
    result = token_response.json()
    access_token_expires = timezone.now() + timedelta(seconds=int(result["expires_in"]))
    refresh_token_expires = timezone.now() + timedelta(
        seconds=int(result["refresh_token_expires_in"])
    )
    t = OauthToken(
        access_token=result["access_token"],
        access_token_expires=access_token_expires,
        refresh_token=result["refresh_token"],
        refresh_token_expires=refresh_token_expires,
    )
    t.save()
    result = t.access_token
    return result


def token_call(data):
    url = f"{settings.INSTANCE}api/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    return requests.post(url, headers=headers, data=data)


def initial_token():
    response = token_call(
        f"grant_type=authorization_code&client_id={settings.HIGHQCLIENTKEY}&client_secret={settings.HIGHQCLIENTSECRET}&code={settings.HIGHQCODE}"
    )

    if response.status_code == 200:
        return save_token_details_and_return(response)


def refresh_token(latest_token):
    response = token_call(
        f"client_id={settings.HIGHQCLIENTKEY}&client_secret={settings.HIGHQCLIENTSECRET}&grant_type=refresh_token&"
        f"refresh_token={latest_token.refresh_token}"
    )

    if response.status_code == 200:
        return save_token_details_and_return(response)
