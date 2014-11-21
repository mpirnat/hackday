from django import forms
from hackday.voting.moremodels import Category, TYPE
from hackday.teams.models import Team, STATUS, PROJECT_TYPE

class VoteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)

        categories = Category.objects.filter(type=TYPE.VOTED).order_by("name")
        for c in categories:
            if c.is_concept:
                queryset=Team.objects.filter(status=STATUS.ACTIVE,
                                project_type=PROJECT_TYPE.CONCEPT).order_by("name")
            elif c.is_implemented:
                queryset=Team.objects.filter(status=STATUS.ACTIVE,
                                project_type=PROJECT_TYPE.IMPLEMENTED).order_by("name")
            else:
                queryset=Team.objects.filter(status=STATUS.ACTIVE).order_by("name")

            self.fields['cat_%s' % c.id] = forms.ModelChoiceField(
                queryset=queryset,
                label=c.name,
                empty_label="Select a team",
                required=False)

class AuthorizeForm(forms.Form):
    user_name = forms.CharField(label='User Name',)
    password = forms.CharField(label='Password', widget=forms.PasswordInput,)

class VoteAuthorizeForm(forms.Form):
    user_name = forms.CharField(label='User Name', widget=forms.TextInput(attrs={'autocapitalize': 'off'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput,)

    def __init__(self, *args, **kwargs):
        super(VoteAuthorizeForm, self).__init__(*args, **kwargs)

        categories = Category.objects.filter(type=TYPE.VOTED).order_by("name")
        for c in categories:
            if c.is_concept:
                queryset=Team.objects.filter(status=STATUS.ACTIVE,
                                project_type=PROJECT_TYPE.CONCEPT).order_by("name")
            elif c.is_implemented:
                queryset=Team.objects.filter(status=STATUS.ACTIVE,
                                project_type=PROJECT_TYPE.IMPLEMENTED).order_by("name")
            else:
                queryset=Team.objects.filter(status=STATUS.ACTIVE).order_by("name")

            self.fields['cat_%s' % c.id] = forms.ModelChoiceField(
                queryset=queryset,
                label=c.name,
                empty_label="Select a team",
                required=False)

