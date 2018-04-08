from django.conf.urls import url
from phone_bill.core.views import add_register, get_phone_bill

urlpatterns = [
    url(r'add_register/$', add_register, name='add_register'),
    url(r'get_phone_bill/$', get_phone_bill, name='get_phone_bill'),
]