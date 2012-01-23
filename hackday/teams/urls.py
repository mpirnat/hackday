from django.conf.urls.defaults import patterns
from django.views.generic import DetailView, ListView

from teams.models import Team


urlpatterns = patterns('',
    (r'^/?$', ListView.as_view(model=Team)),
    (r'^(?P<slug>[\w-]+)/*$', DetailView.as_view(model=Team)),
)
