from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from phone_bill.core.models import Call, PhoneBill


scheduler = BackgroundScheduler()


@scheduler.scheduled_job('cron', id='close_account', day=9, minute=1)
def save_account():
    now = timezone.now()
    month, year = now.month, now.year
    call_ids = Call.objects.filter(
        (Q(timestamp__month=month) & Q(timestamp__year=year)),
        type_call='end'
    ).values_list('call_id', flat=True)
    calls = Call.objects.filter(
        call_id__in=call_ids
    ).order_by('call_id', 'timestamp')
    PhoneBill.objects.generate_accounts(calls, month, year)


scheduler.start()


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            sleep(10000)

