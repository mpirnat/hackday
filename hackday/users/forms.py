from django import forms
from users.models import Tshirt, Diet, Location


class SignUpForm(forms.Form):

    user_name = forms.CharField(label='User Name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email Address')
    tshirt = forms.ModelChoiceField(label='T-Shirt Size',
            queryset=Tshirt.objects.all())
    diet = forms.ModelChoiceField(label='Dietary Preference',
            queryset=Diet.objects.all())
    location = forms.ModelChoiceField(label='Location',
            queryset=Location.objects.all())
    description = forms.CharField(label='Describe Yourself',
            widget=forms.Textarea, required=False)


class SignInForm(forms.Form):

    user_name = forms.CharField(label='User Name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    next = forms.CharField(label='Next URL', widget=forms.HiddenInput)


class UserProfileForm(forms.Form):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email Address')
    tshirt = forms.ModelChoiceField(label='T-Shirt Size',
            queryset=Tshirt.objects.all())
    diet = forms.ModelChoiceField(label='Dietary Preference',
            queryset=Diet.objects.all())
    location = forms.ModelChoiceField(label='Location',
            queryset=Location.objects.all())
    description = forms.CharField(label='Describe Yourself',
            widget=forms.Textarea, required=False)
    password = forms.CharField(label='Password',
            widget=forms.PasswordInput, required=False)

