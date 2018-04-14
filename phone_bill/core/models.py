from datetime import timedelta
from django.db import models
from phone_bill.core.managers import PhoneBillManager


class Call(models.Model):
    TYPE_CALL = (
        ('start', 'Start'),
        ('end', 'End'),
    )
    id = models.AutoField(primary_key=True)
    type_call = models.CharField(max_length=10, choices=TYPE_CALL, null=False)
    timestamp = models.DateTimeField()
    call_id = models.BigIntegerField()
    source = models.CharField(max_length=20, null=True)
    destination = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = 'call'
        verbose_name_plural = 'calls'
        unique_together = (('call_id', 'type_call'), )

    def __str__(self):
        return '{} - {}'.format(self.type_call, self.call_id)


class CallBilling(models.Model):
    destination = models.CharField(max_length=20)
    start_call = models.DateTimeField()
    duration_call = models.FloatField()
    price = models.FloatField()
    phone_bill = models.ForeignKey('PhoneBill', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Call Billing'
        verbose_name_plural = 'Call Billings'

    @staticmethod
    def price_call(start_call, duration_call):
        """
        :return: price
        """
        standing_price = 0.36
        minute_price = 0.09
        price = 0
        end_call = start_call + timedelta(seconds=duration_call)
        while start_call < end_call:
            if 5 <= start_call.hour <= 21:
                new_start = start_call.replace(hour=22, minute=0, second=0)
                if new_start > end_call:
                    new_start = end_call
                seconds = int((new_start - start_call).total_seconds())
                price += minute_price * int(seconds/60)
            else:
                if start_call.hour < 6 or start_call.hour > 22:
                    new_start = start_call.replace(hour=6, minute=0, second=0)
                else:
                    if start_call.hour == 6:
                        new_start = start_call.replace(
                            hour=22, minute=0, second=0
                        )
                    elif start_call.hour == 22:
                        new_start = start_call.replace(
                            hour=6, minute=0, second=0
                        ) + timedelta(days=1)
                if new_start > end_call:
                    new_start = end_call
            start_call = new_start

        price += standing_price
        return price


class PhoneBill(models.Model):
    source = models.CharField(max_length=20)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    amount = models.FloatField()
    objects = PhoneBillManager()

    class Meta:
        verbose_name = 'Phone Bill'
        verbose_name_plural = 'Phone Billings'
        unique_together = (('source', 'month', 'year'), )
