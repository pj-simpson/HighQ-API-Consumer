from django_cron import CronJobBase, Schedule
from .models import OauthToken
from django.db.models import Q

def del_all_but_most_recent_token():
    latest_token_id = OauthToken.objects.latest('gen_time').id
    OauthToken.objects.filter(~Q(id=latest_token_id)).delete()

class OauthCronJob(CronJobBase):
    RUN_EVERY_MINS = 60

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'siteadmin.oauth_cron_job'

    def do(self):
        del_all_but_most_recent_token()


