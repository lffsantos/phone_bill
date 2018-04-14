from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url(r'^api/v1/', include('phone_bill.core.urls')),
]
