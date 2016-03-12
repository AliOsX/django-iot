from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django_iot.apps.devices.models import Device


class DeviceDetailView(DetailView):
    model = Device

    def get_context_data(self, *args, **kwargs):
        # default context
        context = super(DeviceDetailView, self).get_context_data(*args, **kwargs)

        # current status
        try:
            current_status = self.object.powerstatus_set.latest('valid_at')
            if current_status.is_on:
                context['status_message'] = 'on'
            else:
                context['status_message'] = 'off'
            context['status_time'] = current_status.valid_at
        except ObjectDoesNotExist:
            context['status_message'] = '[unknown]'
            context['status_time'] = None

        # return
        return context


class DeviceListView(ListView):
    model = Device
