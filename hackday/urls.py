from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackday.views.home', name='home'),
    # url(r'^hackday/', include('hackday.foo.urls')),

    # Let the blog own the homepage?
    (r'^/*$', 'blog.views.index'),

    # We have a blog!
    (r'^blog/?', include('blog.urls')),

    # List of approved charities
    (r'^charities/?', include('charities.urls')),

    # User stuff - sign up, sign in, sign out, user profiles
    (r'^users/?', include('users.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Arbitrary wiki pages FTW!
    (r'^(?P<path>.*[^/])/?$', 'wiki.views.page'),
)


handler403 = 'common.forbidden'
handler404 = 'common.not_found'
handler500 = 'common.server_error'
