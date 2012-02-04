from django import forms
from teams.models import Team


class EditTeamForm(forms.ModelForm):

    """ Handle both ADDing and UPDATEing.
    """

    class Meta:
        model = Team
        exclude = ('creator', 'images', 'attachments', 'links', 'status')
