import json
from _datetime import datetime

from parameterized import parameterized
from django.test import TestCase

from phone_bill.core.models import Call, CallBilling


class TestCall(TestCase):

    @parameterized.expand([
        (json.dumps(
            {'id': 1, 'source': '12234', 'destination': '122345',
             'type_call': 'start', 'call_id': 1,
             'timestamp': '2017-12-12T15:14:56Z'}
        )),
    ])
    def tests_insert_valid(self, data):
        call = json.loads(data)
        Call.objects.create(**call)
        assert Call.objects.exists()


class TestCallBilling(TestCase):

    @parameterized.expand([
        (json.dumps({
            'start': '12/12/2017 15:07:13',
            'duration': 463,
            'expected_price': 0.99
        })),
        (json.dumps({
            'start': '12/12/2017 22:47:56',
            'duration': 180,
            'expected_price': 0.36,
        })),
        (json.dumps({
            'start': '12/12/2017 21:57:13',
            'duration': 823,
            'expected_price': 0.54,
        })),
        (json.dumps({
            'start': '12/12/2017 4:57:13',
            'duration': 4423,
            'expected_price': 1.26,
        })),
        (json.dumps({
            'start': '12/12/2017 21:57:13',
            'duration': 87223,
            'expected_price': 86.94,
        }))
    ])
    def test_price_call(self, data):
        data = json.loads(data)
        start_date = datetime.strptime(data['start'], '%d/%m/%Y %H:%M:%S')
        price = CallBilling.price_call(start_date, data['duration'])
        self.assertEqual(str(data['expected_price']), "{:.2f}".format(price))
