from django import forms
from hackday.users.models import User, UserProfile
from hackday.teams.models import Team
from hackday.voting.moremodels import Category, TYPE

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return "{0} {1}".format(user.first_name, user.last_name)


class UserMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, user):
        return "{0} {1}".format(user.first_name, user.last_name)


class BaseTeamForm(forms.ModelForm):
    captain = UserChoiceField(queryset=User.objects.filter(
                is_active=True).order_by('first_name', 'last_name'))
    members = UserMultipleChoiceField(queryset=User.objects.filter(
                is_active=True).order_by('first_name', 'last_name'))
    category = forms.ModelChoiceField(queryset=Category.objects.filter(
                type=TYPE.JUDGED).order_by("name"))

    class Meta:
        model = Team
        exclude = ('creator', 'images', 'attachments', 'links', 'status')
        abstract = True

class CreateTeamForm(BaseTeamForm):
    pass


class UpdateTeamForm(BaseTeamForm):
    pass

