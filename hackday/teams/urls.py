from django.conf.urls.defaults import patterns, url

from teams.models import Team, STATUS
from teams.views import delete_team
from teams.views import TeamCreateView
from teams.views import TeamDetailView
from teams.views import TeamListView
from teams.views import TeamUpdateView


urlpatterns = patterns('teams.views',
    url(r'^/?$', TeamListView.as_view(), name='teams-list'),
    url(r'^create/?$', TeamCreateView.as_view(), name='teams-create'),
    url(r'^edit/(?P<slug>[\w-]+)/*$', TeamUpdateView.as_view(),
        name='teams-edit'),
    url(r'^(?P<slug>[\w-]+)/*$', TeamDetailView.as_view(),
        name='teams-detail'),
    url(r'^delete/(?P<team_slug>[\w-]+)/*$', delete_team,
        name='teams-delete'),
)
