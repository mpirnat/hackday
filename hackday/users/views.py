from hackday.common import common_env
from hackday.users.forms import SignUpForm, SignInForm, UserProfileForm
from hackday.users.models import User, UserProfile, Tshirt, Diet, Location
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context, RequestContext, loader


def index(request):
    users = User.objects.exclude(last_name='', first_name='').\
            order_by('last_name', 'first_name', 'username')
    env = common_env()
    env['users'] = users
    return render(request, 'users/index.html', env)


def sign_up(request):
    error_message = None

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
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

                # Create the user profile
                user_profile = UserProfile(
                        user=user,
                        alternate_email=form.cleaned_data['alternate_email'],
                        phone=form.cleaned_data['phone'],
                        tshirt=form.cleaned_data['tshirt'],
                        diet=form.cleaned_data['diet'],
                        location=form.cleaned_data['location'],
                        description=form.cleaned_data['description'],
                        notify_by_email=form.cleaned_data['notify_by_email'])
                user_profile.save()

                # Log the user in
                user = authenticate(username=user.username,
                        password=form.cleaned_data['password'])
                login(request, user)

                return HttpResponseRedirect(reverse('users-profile', args=[user.username])) # Redirect after POST
    else:
        form = SignUpForm()

    env = common_env()
    env['form'] = form
    env['error_message'] = error_message
    return render(request, 'users/signup.html', env)


def sign_out(request):
    logout(request)
    env = common_env()
    return render(request, 'users/signout.html', env)


def sign_in(request):
    error_message = None

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'],
                    password=form.cleaned_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    next_url = form.cleaned_data['next']
                    if not next_url.startswith('/'):
                        raise PermissionDenied
                    return HttpResponseRedirect(next_url)
                else:
                    error_message = "Account disabled"
            else:
                error_message = "Bad username or password"
    else:
        next_url = request.GET.get('next') or reverse('blog-home')
        form = SignInForm(initial={'next': next_url})

    env = common_env()
    env['form'] = form
    env['error_message'] = error_message
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

    if request.user != user:
        raise PermissionDenied

    elif request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']

            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])

            user_profile.alternate_email = form.cleaned_data['alternate_email']
            user_profile.phone = form.cleaned_data['phone']
            user_profile.tshirt = form.cleaned_data['tshirt']
            user_profile.diet = form.cleaned_data['diet']
            user_profile.location = form.cleaned_data['location']
            user_profile.description = form.cleaned_data['description']
            user_profile.notify_by_email = form.cleaned_data['notify_by_email']

            user.save()
            user_profile.save()

            message = 'Updated profile.'

    else:
        form = UserProfileForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'alternate_email': user_profile.alternate_email,
                'phone': user_profile.phone,
                'tshirt': user_profile.tshirt,
                'diet': user_profile.diet,
                'location': user_profile.location,
                'description': user_profile.description,
                'notify_by_email': user_profile.notify_by_email,
        })

    env = common_env()
    env['form'] = form
    env['user_'] = user
    env['message'] = message
    env['user_profile'] = user_profile
    return render(request, 'users/edit_profile.html', env)
