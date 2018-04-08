import json

from django.test import TestCase
from django.shortcuts import resolve_url as r
from rest_framework import status
from parameterized import parameterized
from phone_bill.core.models import Call


class TestRegisterCall(TestCase):

    @parameterized.expand([
        (json.dumps(
            {'id': 1, 'source': '12234', 'destination': '12234', 'call_id': 1,
             'type': 'start',  'timestamp': '2017-12-12T15:14:56Z'}
        )),
        (json.dumps(
            {'id': 1, 'type': 'end', 'call_id': 1,
             'timestamp': '2017-12-12T15:14:56Z'}
        )),
    ])
    def test_add_register_good_request(self, data):
        response = self.client.post(
            r('add_register'), data, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Call.objects.count() == 1)
        result = response.data
        data = json.loads(data)
        for key, value in data.items():
            expected = data[key]
            self.assertEqual(result[key], expected)

    @parameterized.expand([
        (json.dumps({'source': '12234', 'destination': '12234'})),
        (json.dumps({
            'call_id': 1, 'type': 'error', 'timestamp': '2017-12-12T15:14:56Z'
        })),
        (json.dumps({'call_id': 1, 'timestamp': '2017-12-12T15:14:56Z'})),
        (json.dumps({'call_id': 1})),
        (json.dumps({'type': 'start'})),
        (json.dumps({'timestamp': '2017-12-12T15:14:56Z'}))
    ])
    def test_add_register_bad_request(self, data):
        response = self.client.post(
            r('add_register'), data, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Call.objects.exists())


class TestGetAccountCall(TestCase):

    fixtures = ['phone_bill/core/fixtures/core.json']

    expected_account = {
        'source': '99988526423',
        'calls': [
            {'price': 'R$ 0.99', 'start_date': '12/12/2017',
             'start_time': '15:07:13', 'call_duration': '0h:7m:43s',
             'destination': '9993468278'},
            {'price': 'R$ 0.63', 'start_date': '12/12/2017',
             'start_time': '22:47:56', 'call_duration': '0h:3m:0s',
             'destination': '9993468278'},
            {'price': 'R$ 1.52', 'start_date': '12/12/2017',
             'start_time': '21:57:13', 'call_duration': '0h:13m:43s',
             'destination': '9993468278'},
            {'price': 'R$ 0.36', 'start_date': '12/12/2017',
             'start_time': '04:57:13', 'call_duration': '1h:13m:43s',
             'destination': '9993468278'},
            {'price': 'R$ 87.83', 'start_date': '12/12/2017',
             'start_time': '21:57:13', 'call_duration': '24h:13m:43s',
             'destination': '9993468278'},
            {'price': 'R$ 0.72', 'start_date': '12/12/2017',
             'start_time': '15:07:58', 'call_duration': '0h:4m:58s',
             'destination': '9993468278'}],
    }

    @parameterized.expand([
        (json.dumps({'source': '99988526423'})),
    ])
    def test_get_phone_bill(self, data):
        response = self.client.get(r('get_phone_bill'), json.loads(data))
        result = response.data
        for key, value in self.expected_account.items():
            if key == 'calls':
                for i, calls in enumerate(value):
                    for k, v in calls.items():
                        self.assertEqual(v, result['calls'][i][k])
            else:
                self.assertEqual(value, result[key])
