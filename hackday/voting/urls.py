from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('hackday.voting.views',
    url(r'^/?$', 'vote', name="voting-vote"),
    url(r'ipad/?$', 'ipad_vote', name="voting-ipad"),
    url(r'info?$', 'info', name="voting-info"),
    url(r'api?$', 'api', name="voting-api"),
    url(r'api/login?$', 'api_login', name="voting-api-login"),
    url(r'results?$', 'results', name="voting-results"),
)
