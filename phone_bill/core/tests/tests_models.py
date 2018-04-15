import json
from _datetime import datetime

from parameterized import parameterized
from django.test import TestCase

from phone_bill.core.models import Call, CallBilling, Tariff


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
            'tariff': {
                'start_time': '06:00', 'end_time': '22:00',
                'call_charge': 0.09, 'standing_charge': 0.36
            },
            'expected_price': 0.99
        })),
        (json.dumps({
            'start': '12/12/2017 22:47:56',
            'duration': 180,
            'tariff': {
                'start_time': '06:00', 'end_time': '22:00',
                'call_charge': 0.09, 'standing_charge': 0.36
            },
            'expected_price': 0.36,
        })),
        (json.dumps({
            'start': '12/12/2017 21:57:13',
            'duration': 823,
            'tariff': {
                'start_time': '06:00', 'end_time': '22:00',
                'call_charge': 0.09, 'standing_charge': 0.36
            },
            'expected_price': 0.54,
        })),
        (json.dumps({
            'start': '12/12/2017 4:57:13',
            'duration': 4423,
            'tariff': {
                'start_time': '06:00', 'end_time': '22:00',
                'call_charge': 0.09, 'standing_charge': 0.36
            },
            'expected_price': 1.26,
        })),
        (json.dumps({
            'start': '12/12/2017 21:57:13',
            'duration': 87223,
            'tariff': {
                'start_time': '06:00', 'end_time': '22:00',
                'call_charge': 0.09, 'standing_charge': 0.36
            },
            'expected_price': 86.94,
        }))
    ])
    def test_price_call(self, data):
        data = json.loads(data)
        start_date = datetime.strptime(data['start'], '%d/%m/%Y %H:%M:%S')
        tariff = Tariff.objects.create(**data['tariff'])
        price = CallBilling.price_call(start_date, data['duration'], tariff)
        self.assertEqual(str(data['expected_price']), "{:.2f}".format(price))
