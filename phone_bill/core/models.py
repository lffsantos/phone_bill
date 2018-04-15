from datetime import timedelta, datetime, date
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
    def price_call(start_call, duration_call, tariff):
        """
        Calculate price of call
        :param start_call: datetime
        :param duration_call: seconds
        :param tariff: object
        :return: price
        """
        def str_to_time(str_date):
            return datetime.strptime(str_date, '%H:%M').time()

        def reduce_second(date_time):
            return (datetime.combine(
                date(1, 1, 1), date_time
            ) - timedelta(seconds=1)).time()

        standing_price = tariff.standing_charge
        minute_price = tariff.call_charge
        price = 0
        end_call = start_call + timedelta(seconds=duration_call)
        end_time = str_to_time(tariff.end_time)
        start_time = str_to_time(tariff.start_time)
        while start_call < end_call:
            e_hour, e_min = end_time.hour, end_time.minute
            s_hour, s_min = start_time.hour, start_time.minute

            if reduce_second(start_time) <= start_call.time() <= \
                    reduce_second(end_time):
                new_start = start_call.replace(
                    hour=e_hour, minute=e_min, second=0
                )
                if new_start > end_call:
                    new_start = end_call
                seconds = int((new_start - start_call).total_seconds())
                price += minute_price * int(seconds/60)
            else:
                if start_call.time() <= start_time:
                    new_start = start_call.replace(
                        hour=s_hour, minute=s_min, second=0
                    )
                elif start_call.time() >= end_time:
                    new_start = start_call.replace(
                        hour=s_hour, minute=s_min, second=0
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


class Tariff(models.Model):
    start_time = models.CharField(max_length=5, null=False)
    end_time = models.CharField(max_length=5, null=False)
    call_charge = models.FloatField(null=False)
    standing_charge = models.FloatField(null=False)

    class Meta:
        verbose_name = 'Tariff'
        verbose_name_plural = 'Tariffs'
