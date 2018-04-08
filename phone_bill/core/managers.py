from django.db import models


class PhoneBillManager(models.Manager):

    def get_account(self, source, month=None, year=None):
        q_filter = {'source': source}
        if month:
            q_filter['month'] = month
        if year:
            q_filter['year'] = year
        phone_bill = self.filter(**q_filter).last()
        return phone_bill
