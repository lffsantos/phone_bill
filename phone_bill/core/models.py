from django.db import models


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

