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
