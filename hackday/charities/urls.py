from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('hackday.charities.views',
    url(r'^/?$', 'index', name='charities-home'),
    url(r'^suggest/?$', 'suggest', name='charities-suggest'),
)
