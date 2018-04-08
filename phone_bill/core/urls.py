from django.conf.urls import url
from phone_bill.core.views import add_register

urlpatterns = [
    url(r'add_register/$', add_register, name='add_register'),
]