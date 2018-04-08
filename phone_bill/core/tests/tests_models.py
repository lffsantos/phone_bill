import json

from parameterized import parameterized
from django.test import TestCase

from phone_bill.core.models import Call


class TestCall(TestCase):

    @parameterized.expand([
        (json.dumps(
            {'id': 1, 'source': '12234', 'destination': '122345', 'type_call': 'start',
             'call_id': 1, 'timestamp': '2017-12-12T15:14:56Z'}
        )),
    ])
    def tests_insert_valid(self, data):
        call = json.loads(data)
        Call.objects.create(**call)
        assert Call.objects.exists()