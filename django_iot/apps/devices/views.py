from django.views.generic import ListView, DetailView
from django_iot.apps.devices.models import Device


class DeviceDetailView(DetailView):
    model = Device


class DeviceListView(ListView):
    model = Device
