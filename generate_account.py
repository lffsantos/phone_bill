import django
django.setup()
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Q
from django.utils import timezone
from phone_bill.core.models import Call, PhoneBill


scheduler = BackgroundScheduler()


@scheduler.scheduled_job('cron', id='close_account', day=1, minute=1)
def save_account():
    # process account of last month finish
    now = timezone.now() - timedelta(days=1)
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