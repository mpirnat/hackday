from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, CreateView

from teams.models import Team


urlpatterns = patterns('teams.views',
    url(r'^/?$', ListView.as_view(model=Team), name='teams-list'),
    url(r'^create/?$', 'create', name='teams-create'),
    url(r'^(?P<slug>[\w-]+)/*$', DetailView.as_view(model=Team),
        name='teams-detail'),
)
