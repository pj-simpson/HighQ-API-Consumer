import pytz
import requests
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import make_aware

from HighQSysAdmProj import settings
from .models import OauthToken;


#helper function -- is a datetime within 30 seconds of now?
def is_close(a_datetime):
    if (a_datetime - timezone.now()).total_seconds()/60 <= 30:
        return True
    else:
        return False



def token_generation():
    result = {}
    check = OauthToken.objects.filter(gen_time__lte=timezone.now()).count()
    # If there are no OauthToken records in the DB, we use the initial token function.
    if check == 0:
        result['token_result'] = initial_token()

    # If there is at least one record in the DB, we grab the latest and check if it expires soon. If not we use it
    # If it does expire soon (or is in the past) , we call the refresh_token function. The refresh token always expries one year in the future
    if check > 0:
        latest_token = OauthToken.objects.latest('gen_time')
        if not is_close(latest_token.access_token_expires):
            result['token_result'] = {'token': latest_token.access_token}
        else:
            result['token_result'] = refresh_token(latest_token)

    return result

def initial_token():
    result = {}
    url = '{instance}api/oauth2/token'.format(instance=settings.INSTANCE)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = 'grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}'.format(client_id=settings.HIGHQCLIENTKEY,client_secret=settings.HIGHQCLIENTSECRET,code=settings.HIGHQCODE)
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        result = response.json()
        access_token_expires = timezone.now() + timedelta(seconds=int(result["expires_in"]))
        access_token_expires = access_token_expires.strftime('%Y-%m-%d %H:%M')
        t = OauthToken(access_token=result["access_token"], access_token_expires=access_token_expires,refresh_token=result["refresh_token"],gen_time=timezone.now())
        t.save()
        result['token'] = t.access_token

    return result

def refresh_token(latest_token):
    result = {}
    url = '{instance}api/oauth2/token'.format(instance=settings.INSTANCE)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = 'client_id={client_id}&client_secret={client_secret}&grant_type=refresh_token&refresh_token={refresh_token}'.format(client_id=settings.HIGHQCLIENTKEY,client_secret=settings.HIGHQCLIENTSECRET,refresh_token=latest_token.refresh_token)
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        result = response.json()
        access_token_expires = timezone.now() + timedelta(seconds=int(result["expires_in"]))
        access_token_expires = access_token_expires.strftime('%Y-%m-%d %H:%M')
        refresh_token_expires = timezone.now() + timedelta(seconds=int(result["refresh_token_expires_in"]))
        refresh_token_expires = refresh_token_expires.strftime('%Y-%m-%d %H:%M')
        t = OauthToken(access_token=result["access_token"], access_token_expires=access_token_expires,
                       refresh_token=result["refresh_token"], gen_time=timezone.now(),
                       refresh_token_expires=refresh_token_expires)
        t.save()
        result['token'] = t.access_token

    return result



