from django.db import IntegrityError
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from phone_bill.core.models import PhoneBill
from phone_bill.core.serializers import CallSerializer, PhoneBillSerializer


@api_view(['POST'])
def add_register(request):
    payload = request.data
    serializer = CallSerializer(data=payload)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    try:
        serializer.save()
    except IntegrityError:
        return Response({'Already register exist with "id" '}, status=500)

    return Response(serializer.data, status=201)


@api_view(['GET'])
def get_phone_bill(request):
    params = request.query_params
    source = params.get('source')
    if not source:
        return Response({'source': 'this is a required field'}, status=400)
    period = params.get('period')
    month, year = None, None
    if period:
        validator = re.compile(
            "^(1[0-2]|0[1-9]|\d)\/(20\d{2}|19\d{2}|0(?!0)\d|[1-9]\d)$"
        )
        if validator.match(period):
            month, year = params.get('period').split('/')
        else:
            return Response({
                'period': 'The format field is MM/YYYY, please informe a '
                          'valid month/year'
            }, status=400)

    month = int(month) if month else None
    phone_bill = PhoneBill.objects.get_account(
        source=source, month=month, year=year
    )
    if not phone_bill:
        return Response({'calls': [], 'source': source}, status=200)

    serializer = PhoneBillSerializer(phone_bill)
    return Response(serializer.data, status=200)