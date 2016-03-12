from django.conf.urls import url
from django_iot.apps.devices.views import DeviceDetailView, DeviceListView


urlpatterns = [
    url(r'^$', DeviceListView.as_view(), name='device-list'),
    url(r'^(?P<pk>[0-9]+)/$', DeviceDetailView.as_view(), name='device-detail'),
]
