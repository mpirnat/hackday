from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('charities.views',
    (r'^/?$', 'index'),
    (r'^suggest/?$', 'suggest'),
)
