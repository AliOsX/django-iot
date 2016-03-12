from django.views.generic.edit import FormView
from django_iot.apps.interactions import tasks, forms


class BaseInteractionView(FormView):
    def form_valid(self, form):
        print form.cleaned_data

        # run tasks
        for task_name in self.task_names:
            task = getattr(tasks, task_name)
            task(**form.cleaned_data)

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
    task_names = ['pull_data', 'pull_status']
