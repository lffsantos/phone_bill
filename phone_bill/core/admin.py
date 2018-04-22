from django.contrib import admin
from django.contrib.auth.models import User, Group
from phone_bill.core.models import Tariff


admin.site.register(Tariff)

admin.site.unregister(User)
admin.site.unregister(Group)

