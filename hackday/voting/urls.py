from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('voting.views',
    url(r'^/?$', 'vote', name="voting-vote"),
)
