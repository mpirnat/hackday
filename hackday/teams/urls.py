from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, CreateView

from teams.models import Team


urlpatterns = patterns('teams.views',
    (r'^/?$', ListView.as_view(model=Team)),
    url(r'^create/?$', 'create'),
    (r'^(?P<slug>[\w-]+)/*$', DetailView.as_view(model=Team)),
)
