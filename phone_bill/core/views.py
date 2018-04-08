from django.db import IntegrityError
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
        return Response({'Already register exist with "id" '})

    return Response(serializer.data, status=201)


@api_view(['GET'])
def get_phone_bill(request):
    params = request.query_params
    if not params.get('source'):
        return Response({'source': 'this is a required field'}, status=400)
    period = params.get('period')
    month, year = None, None

    phone_bill = PhoneBill.objects.get_account(
        source=params.get('source'), month=month, year=year
    )
    if not phone_bill:
        return Response({'Phone Bill not found'}, status=200)

    serializer = PhoneBillSerializer(phone_bill)
    return Response(serializer.data, status=200)