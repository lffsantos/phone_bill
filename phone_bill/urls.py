from django.conf.urls import url
from django.urls import include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='core/itworks.html'), name='home'),
    url(r'^api/v1/', include('phone_bill.core.urls')),
]
