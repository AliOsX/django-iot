from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django_iot.apps.devices.models import Device
from django_iot.apps.interactions import forms as interaction_forms


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

        # set up forms
        context['forms'] = [
            {
                'form': interaction_forms.BaseInteractionForm(initial={'device_id': self.object.pk}),
                'post_url': reverse('refresh'),
                'btn_message': 'Refresh',
            },
            {
                'form': interaction_forms.SetStatusForm(initial={'device_id': self.object.pk, 'is_on': True}),
                'post_url': reverse('set-status'),
                'btn_message': 'Turn on',
            },
            {
                'form': interaction_forms.SetStatusForm(initial={'device_id': self.object.pk, 'is_on': True}),
                'post_url': reverse('set-status'),
                'btn_message': 'Turn off',
            },
            {
                'form': interaction_forms.SetColorForm(initial={'device_id': self.object.pk}),
                'post_url': reverse('set-color'),
                'btn_message': 'Change color',
            },
        ]

        # return
        return context


class DeviceListView(ListView):
    model = Device
