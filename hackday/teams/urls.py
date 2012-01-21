from django.conf.urls.defaults import patterns, include, url
from teams.views import TeamList, TeamDetail


urlpatterns = patterns('',
    (r'^/?$', TeamList.as_view()),
    (r'^(?P<slug>[\w-]+)/*$', TeamDetail.as_view()),
)
