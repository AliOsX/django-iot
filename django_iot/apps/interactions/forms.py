from django import forms


class BaseInteractionForm(forms.Form):
    device_id = forms.IntegerField(widget=forms.HiddenInput())


class SetStatusForm(BaseInteractionForm):
    is_on = forms.BooleanField(widget=forms.HiddenInput(), required=False)


class SetColorForm(BaseInteractionForm):
    color = forms.CharField(help_text="hex color, eg #fff or #001122")
