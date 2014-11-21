import math
import json
from collections import OrderedDict
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from hackday.voting.forms import VoteForm, AuthorizeForm, VoteAuthorizeForm
from hackday.voting.models import VoteCart, Vote, VoteStatus, STATUS
from hackday.voting.moremodels import Category, TYPE
from hackday.teams.models import Team, STATUS as TEAM_STATUS
from hackday.users.models import User, UserProfile


class DjangoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return json.loads(serializers.serialize('json', obj))
        return JSONEncoder.default(self,obj)

def ipad_vote(request):
    logout(request)
    env = {}

    try:
        online = VoteStatus.objects.all()[0].online
    except:
        online = False

    if not online:
        return render(request, 'voting/vote_offline.html');

    error_message = None
    user = None
    votes = []

    if request.method == 'POST':
        form = VoteAuthorizeForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'],
                                password=form.cleaned_data['password'])
            if user:
                try:
                    cart = VoteCart.objects.get(user=user.id)
                except:
                    cart = VoteCart(user=user, status=STATUS.ACTIVE)
                    cart.save()

                for key,team in form.cleaned_data.items():
                    if key.startswith('cat_'):
                        category_id = key.replace('cat_', '')
                        category = Category.objects.get(id=category_id)
                        _insert_or_update_vote(cart, category, team)
                        votes.append({'category': category, 'team': team})
                env = {'user': user}
                env['votes'] = votes
                return render(request, 'voting/ipad_vote_complete.html', env);
            else:
                error_message = "Bad username or password"
    else:
        form = VoteAuthorizeForm()

    env['form'] = form
    env['error_message'] = error_message
    return render(request, 'voting/ipad_vote.html', env)

@login_required
def vote(request):
    env = {}

    try:
        online = VoteStatus.objects.all()[0].online
    except:
        online = False

    if not online:
        return render(request, 'voting/vote_offline.html');

    try:
        cart = VoteCart.objects.get(user=request.user.id)
    except:
        cart = VoteCart(user=request.user, status=STATUS.ACTIVE)
        cart.save()

    # voting is complete don't allow more votes
    if cart.status == STATUS.COMPLETED:
        return render(request, 'voting/vote_complete.html');

    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():

            for key,team in form.cleaned_data.items():
                category_id = key.replace('cat_', '')
                category = Category.objects.get(id=category_id)
                _insert_or_update_vote(cart, category, team)
            return render(request, 'voting/vote_complete.html');
    else:
        votes = Vote.objects.filter(cart=cart.id)
        form_init = {}
        for vote in votes:
            form_init['cat_%s' % vote.category.id] = vote.team.id
        form = VoteForm(form_init)

    env['form'] = form
    return render(request, 'voting/vote.html', env)


def info(request):
    categories = Category.objects.filter(type=TYPE.VOTED).order_by('id')
    teams = Team.objects.filter(status=TEAM_STATUS.ACTIVE).order_by('id')
    judged = Category.objects.filter(type=TYPE.JUDGED).order_by('id')

    d = {}
    for category in judged:
        d[category.name] = [t for t in teams if t.category.id == category.id]
        d[category.name].sort()

    ordered_teams = []
    o_dict = OrderedDict(sorted(d.items(), key=lambda t: len(t)))
    for item in o_dict.values():
        ordered_teams += item

    env = {'categories': categories,
           'teams': ordered_teams}
    return render(request, 'voting/info.html', env)

@csrf_exempt
def api_login(request):
    env = {'status': 'unauthorized'}

    if request.method == 'POST':
        form = AuthorizeForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'],
                                password=form.cleaned_data['password'])
            if user:
                try:
                    user_profile = UserProfile.objects.get(user=user)
                except:
                    user_profile = None

                if user.is_active and user_profile:
                    login(request, user)
                    env = {'status': 'ok'}

    return HttpResponse(json.dumps(env), mimetype="application/json")


@csrf_exempt
@login_required
def api(request):
    categories = Category.objects.filter(type=TYPE.VOTED).order_by('id')
    teams = Team.objects.filter(status=TEAM_STATUS.ACTIVE).order_by('id')
    users = User.objects.filter(is_active=True).order_by('id')
    judged = Category.objects.filter(type=TYPE.JUDGED).order_by('id')

    saved = False

    try:
        online = VoteStatus.objects.all()[0].online
    except:
        online = False

    try:
        cart = VoteCart.objects.get(user=request.user.id)
    except:
        cart = VoteCart(user=request.user, status=STATUS.ACTIVE)
        cart.save()

    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid() and online:

            for key,team in form.cleaned_data.items():
                category_id = key.replace('cat_', '')
                category = Category.objects.get(id=category_id)
                _insert_or_update_vote(cart, category, team)
            saved = True

    vote_dict = {}
    votes = Vote.objects.filter(cart=cart.id)
    for vote in votes:
        vote_dict[vote.category.id] = vote.team.id

    env = {'categories': categories,
           'judged_categories': judged,
           'teams': teams,
           'users': users,
           'online': online,
           'votes': vote_dict,
           'saved': saved,
           }

    return HttpResponse(json.dumps(env, cls=DjangoJSONEncoder),
                        mimetype="application/json")


@user_passes_test(lambda u: u.is_superuser)
def results(request):
    vote_results = [];

    categories = Category.objects.filter(type=TYPE.VOTED).order_by('id')
    totals = {}
    for t in Vote.objects.values('category').annotate(total=Count('category')):
        totals[t['category']] = t['total']

    for category in categories:
        votes = Vote.objects.filter(category=category).values('team').annotate(
            votes=Count('id')).order_by('votes').reverse()

        votes = [{'votes': v['votes'],
                  'percentage': _get_percentage(v['votes'], totals[category.id]),
                  'team': Team.objects.get(id=v['team'])}
                for v in votes][:10]
        if 'goat' in request.GET.keys():
            _fix_votes(votes, totals[category.id])

        vote_results.append({'category': category,
                             'votes': votes,
                             'total': totals.get(category.id, 0)})

    env = {'vote_results': vote_results}
    return render(request, 'voting/results.html', env)

def _fix_votes(votes, total):
    for idx,vote in enumerate(votes):
        if vote['team'].name == "Bring The Goat":
            goat = votes[idx]
            goat['percentage'] = 100
            goat['votes'] = total
            votes.remove(goat)
            votes.insert(0, goat)
        else:
            votes[idx]['percentage'] = 0
            votes[idx]['votes'] = 0


def _get_percentage(votes, total):
    percent = (1.0 * votes) / (1.0 * total)
    percent = 100 * percent
    return int(math.ceil(percent))

def _insert_or_update_vote(cart, category, team):
    if team is not None and category is not None:
        if ((category.is_concept and team.is_implemented) or
            (category.is_implemented and team.is_concept)):
            raise Exception("invalid concept/implemenation match")

    try:
        vote = Vote.objects.get(cart=cart, category=category)
        if team is None:
            vote.delete()
        else:
            vote.team = team
            vote.save()
    except:
        if team is not None:
            vote = Vote(cart=cart, category=category, team=team)
            vote.save()
