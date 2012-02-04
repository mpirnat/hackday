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
        return super(TeamUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('teams-detail', kwargs={'slug': self.object.slug})


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

        return HttpResponseRedirect(reverse('teams-detail',
            kwargs={'slug': team.slug}))
