import argparse
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from phone_bill.core.models import Call, PhoneBill


def save_account(month, year):
    call_ids = Call.objects.filter(
        (Q(timestamp__month=month) & Q(timestamp__year=year)),
        type_call='end'
    ).values_list('call_id', flat=True)
    calls = Call.objects.filter(
        call_id__in=call_ids
    ).order_by('call_id', 'timestamp')
    PhoneBill.objects.generate_accounts(calls, month, year)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("-m", "--month", help="number between 1-12", type=int)
        parser.add_argument("-y", "--year", type=int)

    def handle(self, *args, **options):
        month, year = options.get('month'), options.get('year')
        if not (month or year):
            print('Please inform a month and year!')
        else:
            now = timezone.now()
            if month >= now.month and year >= now.year:
                print('Please inform a shorter date!')
            else:
                save_account(month, year)
