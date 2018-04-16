from rest_framework import serializers
from phone_bill.core.models import Call, CallBilling, PhoneBill


class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call
        fields = '__all__'

    def create(self, validated_data):
        return Call.objects.create(**validated_data)

    def to_representation(self, instance):
        values = {
            "id": instance.id,
            "type":  instance.type_call,
            "timestamp": str(instance.timestamp),
            "call_id":  instance.call_id,
        }
        if instance.type_call == 'start':
            values.update({
                "source":  instance.source,
                "destination": instance.destination
            })
        return values

    def to_internal_value(self, data):
        type_call = data.get('type')

        if not data.get('id'):
            raise serializers.ValidationError({
                'id': 'This field is required.'
            })
        if not type_call:
            raise serializers.ValidationError({
                'type': 'This field is required.'
            })
        if type_call not in ['start', 'end']:
            raise serializers.ValidationError({
                'type': 'this field must be equals a "start" or "end" value '
            })
        if type_call == 'start' and not data.get('source') and not data.get('destination'):
            raise serializers.ValidationError({
                'error': '{source} and {destination} is required for this type'
            })

        if not data.get('timestamp'):
            raise serializers.ValidationError({
                'timestamp': 'This field is required.'
            })
        if not data.get('call_id'):
            raise serializers.ValidationError({
                'call_id': 'This field is required.'
            })
        if data.get('call_id') and not isinstance(data.get('call_id'), int):
            raise serializers.ValidationError({
                'call_id': 'this field must be a integer format'
            })
        return {
            "id": data.get('id'),
            "type_call":  type_call,
            "timestamp": data.get('timestamp'),
            "call_id":  data.get('call_id'),
            "source":  data.get('source'),
            "destination": data.get('destination')
        }


class PhoneBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneBill
        fields = '__all__'

    def to_representation(self, instance):
        result = {
            'source': instance.source,
            'calls': [],
            "period": '{}/{}'.format(instance.month, instance.year),
            "amount": instance.amount
        }
        for call in instance.callbilling_set.all().order_by('start_call'):
            call_serializer = CallBillingSerializer(call).data
            result['calls'].append(call_serializer)

        return result


class CallBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallBilling
        fields = '__all__'

    def to_representation(self, instance):
        def format_call_duration(seconds):
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds %= 60
            return '{}h:{}m:{}s'.format(int(hours), int(minutes), int(seconds))

        values = {
            "destination": instance.destination,
            "start_date":  instance.start_call.strftime("%d/%m/%Y"),
            "start_time": instance.start_call.strftime("%H:%M:%S"),
            "call_duration":  str(format_call_duration(
                int(instance.duration_call)
            )),
            "price":  'R$ {}'.format(instance.price),
        }
        return values
