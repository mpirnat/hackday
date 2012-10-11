from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('hackday.voting.views',
    url(r'^/?$', 'vote', name="voting-vote"),
    url(r'info?$', 'info', name="voting-info"),
    url(r'results?$', 'results', name="voting-results"),
)
