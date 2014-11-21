from django import forms
from hackday.messaging.models import RSVP

class RSVPForm(forms.Form):
    email = forms.EmailField(label='My Email Address',)
    will_attend = forms.BooleanField(
            label="Yes I do plan to attend the Hack Day presentations", required=False)
