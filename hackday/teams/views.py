from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from teams.forms import CreateTeamForm
from teams.models import Team, STATUS


@login_required()
def create(request):

    form = CreateTeamForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        team = form.save(commit=False)
        team.status = STATUS.ACTIVE
        team.creator = request.user
        team.save()
        form.save_m2m()

        return HttpResponseRedirect('/teams/' + team.slug)

    return render(request, 'teams/team_form.html', {'form': form})
