from django.db.models import Q

from .models import OauthToken


def oauth_cron_clearout():
    latest_token_id = OauthToken.objects.latest("gen_time").id
    OauthToken.objects.filter(~Q(id=latest_token_id)).delete()
