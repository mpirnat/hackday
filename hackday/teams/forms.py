from django import forms
from teams.models import Team


class CreateTeamForm(forms.ModelForm):

    class Meta:
        model = Team
        exclude = ('creator', 'images', 'attachments', 'links', 'status')
