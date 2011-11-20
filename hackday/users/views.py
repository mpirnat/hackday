from users.forms import SignUpForm, SignInForm, UserProfileForm
from users.models import User, UserProfile, Tshirt, Diet, Location
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader


def index(request):
    users = User.objects.order_by('last_name').order_by('first_name').order_by('username')

    t = loader.get_template('users/index.html')
    c = RequestContext(request, {
        'users': users
    })

    return HttpResponse(t.render(c))


def sign_up(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                    form.cleaned_data['user_name'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password'])

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # Create the user profile
            user_profile = UserProfile(
                    user=user,
                    tshirt=form.cleaned_data['tshirt'],
                    diet=form.cleaned_data['diet'],
                    location=form.cleaned_data['location'],
                    description=form.cleaned_data['description'])
            user_profile.save()

            # Log the user in
            user = authenticate(username=user.username,
                    password=form.cleaned_data['password'])
            login(request, user)

            return HttpResponseRedirect('/users') # Redirect after POST
    else:
        form = SignUpForm()

    t = loader.get_template('users/signup.html')
    c = RequestContext(request, {
        'form': form,
    })

    return HttpResponse(t.render(c))


def sign_out(request):

    logout(request)

    t = loader.get_template('users/signout.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))


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
        next_url = request.GET.get('next') or '/users'
        form = SignInForm(initial={'next': next_url})

    t = loader.get_template('users/signin.html')
    c = RequestContext(request, {
        'form': form,
        'error_message': error_message,
    })
    return HttpResponse(t.render(c))


def profile(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)

    t = loader.get_template('users/profile.html')
    c = RequestContext(request, {
        'user_': user,
        'user_profile': user_profile,
    })
    return HttpResponse(t.render(c))


@login_required(login_url='/users/sign-in')
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
            
            user_profile.tshirt = form.cleaned_data['tshirt']
            user_profile.diet = form.cleaned_data['diet']
            user_profile.location = form.cleaned_data['location']
            user_profile.description = form.cleaned_data['description']
            
            user.save()
            user_profile.save()

            message = 'Updated profile.'

    else:
        data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'tshirt': user_profile.tshirt,
                'diet': user_profile.diet,
                'location': user_profile.location,
                'description': user_profile.description,
        }
        form = UserProfileForm(initial=data)

    t = loader.get_template('users/edit_profile.html')
    c = RequestContext(request, {
        'form': form,
        'user_': user,
        'message': message,
    })
    return HttpResponse(t.render(c))
