from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

from teams.models import Team

urlpatterns = patterns('teams.views',
    (r'^/?', ListView.as_view(model=Team)),
)
