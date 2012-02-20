from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView
from teams.models import Team, STATUS
from teams.views import TeamUpdateView, TeamCreateView, delete_team


urlpatterns = patterns('teams.views',
    url(r'^/?$', ListView.as_view(model=Team,
            queryset=Team.objects.filter(status=STATUS.ACTIVE)),
        name='teams-list'),
    url(r'^create/?$', TeamCreateView.as_view(), name='teams-create'),
    url(r'^edit/(?P<slug>[\w-]+)/*$', TeamUpdateView.as_view(
            queryset=Team.objects.filter(status=STATUS.ACTIVE)),
        name='teams-edit'),
    url(r'^(?P<slug>[\w-]+)/*$', DetailView.as_view(model=Team,
            queryset=Team.objects.filter(status=STATUS.ACTIVE)),
        name='teams-detail'),
    url(r'^delete/(?P<team_slug>[\w-]+)/*$', delete_team,
        name='teams-delete'),
)
