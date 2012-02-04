from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView
from teams.models import Team
from teams.views import TeamUpdateView, TeamCreateView


urlpatterns = patterns('teams.views',
    url(r'^/?$', ListView.as_view(model=Team), name='teams-list'),
    url(r'^create/?$', TeamCreateView.as_view(), name='teams-create'),
    url(r'^edit/(?P<slug>[\w-]+)/*$', TeamUpdateView.as_view(),
        name='teams-edit'),
    url(r'^(?P<slug>[\w-]+)/*$', DetailView.as_view(model=Team),
        name='teams-detail'),
)
