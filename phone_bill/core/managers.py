from django.db import models


class PhoneBillManager(models.Manager):

    def get_account(self, source, month=None, year=None):
        """ Get phone bill account """
        q_filter = {'source': source}
        if month:
            q_filter['month'] = month
        if year:
            q_filter['year'] = year
        phone_bill = self.filter(**q_filter).last()
        return phone_bill

    def generate_accounts(self, calls, month, year):
        """
        :param calls: list of calls(ordered by (call_id, timestamp))
        :param month: MM
        :param year: YYYY
        """
        from phone_bill.core.models import CallBilling

        source = {}
        last_source = None
        for call in calls:
            if call.source and call.source not in source:
                source[call.source] = []
                last_source = call.source
            if call.type_call == 'start':
                source[call.source].append({
                    'destination': call.destination, 'start_date': call.timestamp
                })
            else:
                source[last_source][-1].update({'end_date': call.timestamp})

        for key, values in source.items():
            if self.get_account(source=key, month=month, year=year):
                continue

            phone_bill = self.create(
                source=key, month=month, year=year, amount=0,
            )
            amount = 0
            for v in values:
                duration = (v['end_date'] - v['start_date']).total_seconds()
                price = CallBilling.price_call(v['start_date'], int(duration))
                data = {
                    'destination': v['destination'],
                    'duration_call': duration,
                    'start_call': v['start_date'],
                    'price': price,
                }
                amount += price
                phone_bill.callbilling_set.create(**data)

            phone_bill.amount = amount
            phone_bill.save()
