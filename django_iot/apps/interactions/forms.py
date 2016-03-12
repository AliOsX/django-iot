from django import forms


class BaseInteractionForm(forms.Form):
    device_id = forms.IntegerField(widget=forms.HiddenInput())


class SetStatusForm(BaseInteractionForm):
    is_on = forms.BooleanField(widget=forms.HiddenInput())


class SetColorForm(BaseInteractionForm):
    color = forms.ChoiceField(choices=[
        ('red', 'red'),
        ('blue', 'blue'),
    ])
