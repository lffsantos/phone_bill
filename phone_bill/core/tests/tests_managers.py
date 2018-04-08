import json

from django.db.models import Q
from django.test import TestCase
from parameterized import parameterized
from phone_bill.core.models import PhoneBill, Call


class TestPhoneBillManager(TestCase):

    calls = [
        {'id': 1, 'destination': '9993468278', 'type_call': 'start',
         'call_id': 71, 'source': '99988526423',
         'timestamp': '2017-12-12 15:07:13+00:00'},
        {'id': 2, 'timestamp': '2017-12-12 15:14:56+00:00', 'type_call': 'end',
         'call_id': 71},
        {'id': 3, 'destination': '9993468278', 'type_call': 'start',
         'call_id': 72, 'source': '99988526423',
         'timestamp': '2017-12-12 22:47:56+00:00'},
        {'id': 4, 'timestamp': '2017-12-12 22:50:56+00:00', 'type_call': 'end',
         'call_id': 72},
        {'id': 5, 'destination': '9993468278', 'type_call': 'start',
         'call_id': 73, 'source': '99988526423',
         'timestamp': '2017-12-12 21:57:13+00:00'},
        {'id': 6, 'timestamp': '2017-12-12 22:10:56+00:00', 'type_call': 'end',
         'call_id': 73},
        {'id': 7, 'destination': '9993468278', 'type_call': 'start',
         'call_id': 74, 'source': '99988526423',
         'timestamp': '2017-12-12 04:57:13+00:00'},
        {'id': 8, 'timestamp': '2017-12-12 06:10:56+00:00', 'type_call': 'end',
         'call_id': 74},
        {'id': 9, 'destination': '9993468278', 'type_call': 'start',
         'call_id': 75, 'source': '99988526423',
         'timestamp': '2017-12-12 21:57:13+00:00'},
        {'id': 10, 'timestamp': '2017-12-13 22:10:56+00:00', 'type_call': 'end',
         'call_id': 75},
        {'id': 11, 'destination': '9993468278', 'type_call': 'start',
         'call_id': 76, 'source': '99988526423',
         'timestamp': '2017-12-12 15:07:58+00:00'},
        {'id': 12, 'timestamp': '2017-12-12 15:12:56+00:00', 'type_call': 'end',
         'call_id': 76}
    ]

    def setUp(self):
        for call in self.calls:
            Call.objects.create(**call)

    @parameterized.expand([
        (json.dumps({
            'month': 12, 'year': 2017, 'source': '99988526423',
            'expected_amount': 90.81
        })),
        (json.dumps({
            'month': 11, 'year': 2016, 'source': '99988526423'
        })),
    ])
    def test_generate_accounts(self, data):
        data = json.loads(data)
        month, year, source = data['month'], data['year'], data['source']
        calls = Call.objects.filter(
            Q(timestamp__month=month) & Q(timestamp__year=year)
        ).order_by('call_id', 'timestamp')
        PhoneBill.objects.generate_accounts(calls, month, year)
        if not data.get('expected_amount'):
            phone_bill = PhoneBill.objects.filter(source=source).last()
            self.assertFalse(phone_bill)
        else:
            phone_bill = PhoneBill.objects.get(source=source)
            self.assertEqual(phone_bill.amount, data['expected_amount'])
