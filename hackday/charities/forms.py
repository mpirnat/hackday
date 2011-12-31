from django import forms
from charities.models import Charity


class SuggestCharityForm(forms.Form):
    name = forms.CharField(label='Charity Name')
    url = forms.URLField(label='Website')
    description = forms.CharField(label='Description', widget=forms.Textarea)

