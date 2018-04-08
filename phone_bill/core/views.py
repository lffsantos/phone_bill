from psycopg2._psycopg import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from phone_bill.core.serializers import CallSerializer


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