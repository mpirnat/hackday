import math
from django.shortcuts import render
from django.db.models import Count
from voting.forms import VoteForm
from voting.models import VoteCart, Vote, VoteStatus, STATUS
from voting.moremodels import Category, TYPE
from teams.models import Team, STATUS as TEAM_STATUS
from django.contrib.auth.decorators import login_required, user_passes_test

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

    env = {'categories': categories,
           'teams': teams}
    return render(request, 'voting/info.html', env)

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
                for v in votes]
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
