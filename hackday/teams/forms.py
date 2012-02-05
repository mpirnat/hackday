from django import forms
from teams.models import Team


class BaseTeamForm(forms.ModelForm):

    class Meta:
        model = Team
        exclude = ('creator', 'images', 'attachments', 'links', 'status')
        abstract = True


class CreateTeamForm(BaseTeamForm):
    pass


class UpdateTeamForm(BaseTeamForm):
    pass
