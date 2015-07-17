from django import forms
from django.contrib.localflavor.us import forms as us_forms
from hackday.users.models import Tshirt, Diet, Location

USERNAME_MESSAGES = {'required': 'Please enter a user name.',
                     'invalid': 'Please enter a user name containing only letters, numbers, underscores, and hyphens.'}

AD_USERNAME_MESSAGES = {'required': 'Please enter a user name.',
                        'invalid': 'Please enter a valid username.'}

EMAIL_MESSAGES = {'required': 'Please enter an email address.',
                  'invalid': 'Please enter a valid email address.'}

ALTERNATE_EMAIL_MESSAGES ={'required': 'Please enter an alternate email address.',
                           'invalid': 'Please enter a valid alternate email address.'}

PASSWORD_MESSAGES = {'required': 'Please enter a password.',
                     'invalid': 'Please enter a valid password.'}

PHONE_MESSAGES = {'required': 'Please enter a mobile phone number.',
                  'invalid': 'Please enter a valid mobile phone number.'}

SHIRT_MESSAGES = {'required': 'Please select a t-shirt size.'}

DIET_MESSAGES = {'required': 'Please select a dietary preference.'}

LOCATION_MESSAGES = {'required': 'Please select a location.'}

FIRST_NAME_MESSAGES = {'required': 'Please enter a first name.',
                       'invalid': 'Please enter a valid first name.'}

LAST_NAME_MESSAGES = {'required': 'Please enter a last name.',
                      'invalid': 'Please enter a valid last name.'}

class ActiveDirectorySignUpForm(forms.Form):
    required_css_class = 'required'

    user_name = forms.CharField(label='User Name',
            error_messages=AD_USERNAME_MESSAGES)
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
            error_messages=PASSWORD_MESSAGES)
    alternate_email = forms.EmailField(label='Alternate Email Address (voting)', required=False,
            error_messages=ALTERNATE_EMAIL_MESSAGES)
    phone = us_forms.USPhoneNumberField(label="Mobile Phone (voting)", required=False,
            error_messages=PHONE_MESSAGES)
    tshirt = forms.ModelChoiceField(label='T-Shirt Size',
            error_messages=SHIRT_MESSAGES,
            queryset=Tshirt.objects.all())
    diet = forms.ModelChoiceField(label='Dietary Preference',
            error_messages=DIET_MESSAGES,
            queryset=Diet.objects.all())
    location = forms.ModelChoiceField(label='Location',
            error_messages=LOCATION_MESSAGES,
            queryset=Location.objects.all())
    description = forms.CharField(label='Describe Yourself',
            widget=forms.Textarea, required=False)
    notify_by_email = forms.BooleanField(
            label="Email me when there's a new post", required=False)
    dinner_required = forms.BooleanField(
            label="I will be staying for dinner on Thursday", required=False)
    breakfast_required = forms.BooleanField(
            label="I will be having breakfast on Friday", required=False)


class ActiveDirectoryUserProfileForm(forms.Form):
    required_css_class = 'required'

    alternate_email = forms.EmailField(label='Alternate Email Address (voting)', required=False,
                                       error_messages=ALTERNATE_EMAIL_MESSAGES)
    phone = us_forms.USPhoneNumberField(label="Mobile Phone (voting)", required=False,
                                        error_messages=PHONE_MESSAGES)
    tshirt = forms.ModelChoiceField(label='T-Shirt Size',
                                    error_messages=SHIRT_MESSAGES,
                                    queryset=Tshirt.objects.all())
    diet = forms.ModelChoiceField(label='Dietary Preference',
                                  error_messages=DIET_MESSAGES,
                                  queryset=Diet.objects.all())
    location = forms.ModelChoiceField(label='Location',
                                      error_messages=LOCATION_MESSAGES,
                                      queryset=Location.objects.all())
    description = forms.CharField(label='Describe Yourself',
            widget=forms.Textarea, required=False)
#    notes = forms.CharField(label='Mission Notes',
#            widget=forms.Textarea, required=False)
    notify_by_email = forms.BooleanField(
            label="Email me when there's a new post", required=False)
    dinner_required = forms.BooleanField(
            label="I will be staying for dinner on Thursday", required=False)
    breakfast_required = forms.BooleanField(
            label="I will be having breakfast on Friday", required=False)


class ActiveDirectorySignInForm(forms.Form):
    required_css_class = 'required'

    user_name = forms.CharField(label='User Name',
            error_messages=AD_USERNAME_MESSAGES)
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
                               error_messages=PASSWORD_MESSAGES)
    next = forms.CharField(label='Next URL', widget=forms.HiddenInput)


class SignUpForm(forms.Form):
    required_css_class = 'required'

    user_name = forms.SlugField(label='User Name',
            error_messages=USERNAME_MESSAGES)
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
                               error_messages=PASSWORD_MESSAGES)
    first_name = forms.CharField(label='First Name',
                               error_messages=FIRST_NAME_MESSAGES)
    last_name = forms.CharField(label='Last Name',
                                error_messages=LAST_NAME_MESSAGES)
    email = forms.EmailField(label='Email Address',
                             error_messages=EMAIL_MESSAGES)
    alternate_email = forms.EmailField(label='Alternate Email Address (voting)', required=False,
                                       error_messages=ALTERNATE_EMAIL_MESSAGES)
    phone = us_forms.USPhoneNumberField(label="Mobile Phone (voting)", required=False,
                                        error_messages=PHONE_MESSAGES)
    tshirt = forms.ModelChoiceField(label='T-Shirt Size',
                                    error_messages=SHIRT_MESSAGES,
                                    queryset=Tshirt.objects.all())
    diet = forms.ModelChoiceField(label='Dietary Preference',
                                  error_messages=DIET_MESSAGES,
                                  queryset=Diet.objects.all())
    location = forms.ModelChoiceField(label='Location',
                                      error_messages=LOCATION_MESSAGES,
                                      queryset=Location.objects.all())
    description = forms.CharField(label='Describe Yourself',
            widget=forms.Textarea, required=False)
    notify_by_email = forms.BooleanField(
            label="Email me when there's a new post", required=False)
    dinner_required = forms.BooleanField(
            label="I will be staying for dinner on Thursday", required=False)
    breakfast_required = forms.BooleanField(
            label="I will be having breakfast on Friday", required=False)


class SignInForm(forms.Form):
    required_css_class = 'required'

    user_name = forms.SlugField(label='User Name',
            error_messages=USERNAME_MESSAGES)
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
                               error_messages=PASSWORD_MESSAGES)
    next = forms.CharField(label='Next URL', widget=forms.HiddenInput)


class UserProfileForm(forms.Form):
    required_css_class = 'required'

    first_name = forms.CharField(label='First Name',
                                 error_messages=FIRST_NAME_MESSAGES)
    last_name = forms.CharField(label='Last Name',
                                error_messages=LAST_NAME_MESSAGES)
    email = forms.EmailField(label='Email Address',
                             error_messages=EMAIL_MESSAGES)
    alternate_email = forms.EmailField(label='Alternate Email Address (voting)', required=False,
                                       error_messages=ALTERNATE_EMAIL_MESSAGES)
    phone = us_forms.USPhoneNumberField(label="Mobile Phone (voting)", required=False,
                                        error_messages=PHONE_MESSAGES)
    tshirt = forms.ModelChoiceField(label='T-Shirt Size',
                                    error_messages=SHIRT_MESSAGES,
                                    queryset=Tshirt.objects.all())
    diet = forms.ModelChoiceField(label='Dietary Preference',
                                  error_messages=DIET_MESSAGES,
                                  queryset=Diet.objects.all())
    location = forms.ModelChoiceField(label='Location',
                                      error_messages=LOCATION_MESSAGES,
                                      queryset=Location.objects.all())
    description = forms.CharField(label='Describe Yourself',
            widget=forms.Textarea, required=False)
#    notes = forms.CharField(label='Mission Notes',
#            widget=forms.Textarea, required=False)
    notify_by_email = forms.BooleanField(
            label="Email me when there's a new post", required=False)
    dinner_required = forms.BooleanField(
            label="I will be staying for dinner on Thursday", required=False)
    breakfast_required = forms.BooleanField(
            label="I will be having breakfast on Friday", required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
                               error_messages=PASSWORD_MESSAGES, required=False)
