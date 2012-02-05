from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView
from teams.forms import EditTeamForm
from teams.models import Team, STATUS


class TeamUpdateView(UpdateView):
    model = Team
    form_class = EditTeamForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """ If user isn't a team member, redirect to team listing.
        """
        response = super(TeamUpdateView, self).dispatch(*args, **kwargs)
        if not self.object.is_member(self.request.user):
            return HttpResponseRedirect(reverse('teams-list'))
        return response

    def form_valid(self, form):
        """ In case the user forgets, add the captain as a team member.
        """
        team = form.save()
        team.add_captain_as_member()

        return HttpResponseRedirect(reverse('teams-detail',
            kwargs={'slug': team.slug}))


class TeamCreateView(CreateView):
    model = Team
    form_class = EditTeamForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """ Because team doesn't exist in DB yet, and creator is required,
            we need to first save the form, add creator, and THEN save to DB
        """
        team = form.save(commit=False)
        team.status = STATUS.ACTIVE
        team.creator = self.request.user
        team.save()
        form.save_m2m()
        team.add_captain_as_member()

        return HttpResponseRedirect(reverse('teams-detail',
            kwargs={'slug': team.slug}))
