import json

from django.test import TestCase
from django.shortcuts import resolve_url as r
from rest_framework import status
from parameterized import parameterized
from phone_bill.core.models import Call


class TestCall(TestCase):

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
        (json.dumps({'call_id': 1, 'type': 'error', 'timestamp': '2017-12-12T15:14:56Z'})),
        (json.dumps({'call_id': 1, 'timestamp': '2017-12-12T15:14:56Z'})),
        (json.dumps({'call_id': 1})),
        (json.dumps({'type': 'start'})),
        (json.dumps({'timestamp': '2017-12-12T15:14:56Z'}))
    ])
    def test_add_register_bad_request(self, data):
        response = self.client.post(r('add_register'), data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Call.objects.exists())
