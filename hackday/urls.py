from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from teams.models import Team

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackday.views.home', name='home'),
    # url(r'^hackday/', include('hackday.foo.urls')),

    (r'^teams/?', ListView.as_view(model=Team)),

    # Let the blog own the homepage?
    (r'^/*$', 'blog.views.index'),

    # We have a blog!
    (r'^blog/?', include('blog.urls')),

    # List of approved charities
    (r'^charities/?', include('charities.urls')),

    # User stuff - sign up, sign in, sign out, user profiles
    (r'^users/reset-password/?$', 'django.contrib.auth.views.password_reset',
        {
            'template_name': 'users/password_reset_form.html',
            'email_template_name': 'users/password_reset_email.html',
        }),
    (r'^users/reset-password/requested/?$',
        'django.contrib.auth.views.password_reset_done',
        {
            'template_name': 'users/password_reset_done.html',
        }),
    (r'^users/reset-password/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/?$',
        'django.contrib.auth.views.password_reset_confirm',
        {
            'template_name': 'users/password_reset_confirm.html'
        }),
    (r'^users/reset-password/done/?$',
        'django.contrib.auth.views.password_reset_complete',
        {
            'template_name': 'users/password_reset_complete.html'
        }),

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
