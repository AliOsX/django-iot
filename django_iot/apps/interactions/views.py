from django.views.generic.edit import FormView
from django_iot.apps.interactions import tasks, forms
from django_iot.apps.devices.models import Device


class BaseInteractionView(FormView):
    template_name = 'interactions/form.html'

    def form_valid(self, form):
        # run tasks
        for task_name in self.task_names:
            task = getattr(tasks, task_name)
            task(**form.cleaned_data)

        # set success url using form data
        device_id = form.cleaned_data['device_id']
        self.success_url = Device.objects.get(pk=device_id).get_absolute_url()

        # return
        return super(BaseInteractionView, self).form_valid(form)


class SetStatus(BaseInteractionView):
    form_class = forms.SetStatusForm
    task_names = ['set_status']


class SetColor(BaseInteractionView):
    form_class = forms.SetColorForm
    task_names = ['set_attributes']


class Refresh(BaseInteractionView):
    form_class = forms.BaseInteractionForm
    task_names = ['pull_attributes', 'pull_status']
