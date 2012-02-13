from django import forms
from voting.moremodels import Category, TYPE
from teams.models import Team, STATUS

class VoteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)

        categories = Category.objects.filter(type=TYPE.VOTED).order_by("name")
        for c in categories:
            self.fields['cat_%s' % c.id] = forms.ModelChoiceField(
                queryset=Team.objects.filter(status=STATUS.ACTIVE).order_by("name"),
                label=c.name,
                empty_label="Select a team",
                required=True)

