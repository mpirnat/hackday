from hackday.common import common_env
from hackday.users.forms import (SignUpForm, SignInForm, UserProfileForm,
    ActiveDirectorySignUpForm, ActiveDirectoryUserProfileForm,
    ActiveDirectorySignInForm)
from hackday.users.models import User, UserProfile, Tshirt, Diet, Location
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context, RequestContext, loader
from django.conf import settings

def index(request):
    users = User.objects.exclude(last_name='', first_name='').\
            order_by('last_name', 'first_name', 'username')
    env = common_env()
    env['users'] = users
    return render(request, 'users/index.html', env)


def sign_up(request):
    error_message = None
    backends = settings.AUTHENTICATION_BACKENDS
    form_class = SignUpForm
    create_user = True

    # the AD backend makes users on login and fills in name and email for us
    # so we don't need those fields on the form
    if 'hackday.auth.backend.ActiveDirectoryBackend' in backends:
        form_class = ActiveDirectorySignUpForm
        create_user = False

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            if create_user:
                # Create the user
                try:
                    user = User.objects.create_user(
                            form.cleaned_data['user_name'],
                            form.cleaned_data['email'],
                            form.cleaned_data['password'])
                except IntegrityError:
                    error_message = "That username is not available."
                else:
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.save()
            else:
                user = authenticate(username=form.cleaned_data['user_name'],
                    password=form.cleaned_data['password'])
                if not user:
                    error_message = "Invalid username or password."

            if not error_message:
                # Create the user profile
                user_profile = UserProfile(
                        user=user,
                        alternate_email=form.cleaned_data['alternate_email'],
                        phone=form.cleaned_data['phone'],
                        tshirt=form.cleaned_data['tshirt'],
                        diet=form.cleaned_data['diet'],
                        location=form.cleaned_data['location'],
                        description=form.cleaned_data['description'],
                        notify_by_email=form.cleaned_data['notify_by_email'],
                        dinner_required=form.cleaned_data['dinner_required'],
                        breakfast_required=form.cleaned_data['breakfast_required'])
                try:
                    user_profile.save()
                except IntegrityError:
                    error_message = "That user has already registered."
                else:
                    # Log the user in
                    user = authenticate(username=user.username,
                            password=form.cleaned_data['password'])
                    login(request, user)

                    return HttpResponseRedirect(reverse('users-profile', args=[user.username])) # Redirect after POST
    else:
        form = form_class()

    env = common_env()
    env['ldap_enabled'] = not create_user
    env['form'] = form
    env['error_message'] = error_message
    return render(request, 'users/signup.html', env)


def sign_out(request):
    logout(request)
    env = common_env()
    return render(request, 'users/signout.html', env)


def sign_in(request):
    error_message = None
    backends = settings.AUTHENTICATION_BACKENDS
    form_class = SignInForm
    ldap_enabled = False
    site = Site.objects.get_current()

    if 'hackday.auth.backend.ActiveDirectoryBackend' in backends:
        form_class = ActiveDirectorySignInForm
        ldap_enabled = True

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'],
                    password=form.cleaned_data['password'])
            if user:
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user.is_active and user_profile:
                        login(request, user)
                        next_url = form.cleaned_data['next']
                        if not next_url.startswith('/'):
                            raise PermissionDenied
                        return HttpResponseRedirect(next_url)
                    else:
                        error_message = "Account disabled"
                except:
                    error_message = "You must sign up before signing in"
            else:
                error_message = "Bad username or password"
    else:
        next_url = request.GET.get('next') or reverse('blog-home')
        form = form_class(initial={'next': next_url})

    backends = settings.AUTHENTICATION_BACKENDS
    env = common_env()
    env['form'] = form
    env['error_message'] = error_message
    env['ldap_enabled'] = ldap_enabled
    env['site_name'] = site.name

    return render(request, 'users/signin.html', env)

@login_required
def profile_redirect(request):
    return HttpResponseRedirect(reverse('users-profile',
                                        args=[request.user.username]))

def profile(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    env = common_env()
    env['user_'] = user
    env['user_profile'] = user_profile
    return render(request, 'users/profile.html', env)


@login_required()
def edit_profile(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    message = None

    form_class = UserProfileForm
    backends = settings.AUTHENTICATION_BACKENDS
    update_user = True

    if 'hackday.auth.backend.ActiveDirectoryBackend' in backends:
        form_class = ActiveDirectoryUserProfileForm
        update_user = False

    if request.user != user:
        raise PermissionDenied

    elif request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            if update_user:
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']

                if form.cleaned_data['password']:
                    user.set_password(form.cleaned_data['password'])

                user.save()

            user_profile.alternate_email = form.cleaned_data['alternate_email']
            user_profile.phone = form.cleaned_data['phone']
            user_profile.tshirt = form.cleaned_data['tshirt']
            user_profile.diet = form.cleaned_data['diet']
            user_profile.location = form.cleaned_data['location']
            user_profile.description = form.cleaned_data['description']
#            user_profile.notes = form.cleaned_data['notes']
            user_profile.notify_by_email = form.cleaned_data['notify_by_email']
            user_profile.dinner_required = form.cleaned_data['dinner_required']
            user_profile.breakfast_required = form.cleaned_data['breakfast_required']

            user_profile.save()

            message = 'Updated profile.'

    else:
        form = form_class(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'alternate_email': user_profile.alternate_email,
                'phone': user_profile.phone,
                'tshirt': user_profile.tshirt,
                'diet': user_profile.diet,
                'location': user_profile.location,
                'description': user_profile.description,
#                'notes': user_profile.notes,
                'notify_by_email': user_profile.notify_by_email,
                'dinner_required': user_profile.dinner_required,
                'breakfast_required': user_profile.breakfast_required,
        })

    env = common_env()
    env['form'] = form
    env['user_'] = user
    env['message'] = message
    env['user_profile'] = user_profile
    return render(request, 'users/edit_profile.html', env)
