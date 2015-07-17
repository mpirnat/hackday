from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Serve uploaded media during development
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Enable debug toolbar in debug mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'hackday.views.home', name='home'),
    # url(r'^hackday/', include('hackday.foo.urls')),

    (r'^teams/', include('hackday.teams.urls')),

    # Let the blog own the homepage?
    url(r'^/*$', 'hackday.blog.views.index', name='blog-home'),

    # We have a blog!
    (r'^blog/', include('hackday.blog.urls')),

    # We have voting!
    (r'^vote/', include('hackday.voting.urls')),

    # List of approved charities
    (r'^charities/', include('hackday.charities.urls')),

    # User stuff - sign up, sign in, sign out, user profiles
    url(r'^users/reset-password/?$', 'django.contrib.auth.views.password_reset',
        {
            'template_name': 'users/password_reset_form.html',
            'email_template_name': 'users/password_reset_email.html',
        }, name='reset-password'),
    url(r'^users/reset-password/requested/?$',
        'django.contrib.auth.views.password_reset_done',
        {
            'template_name': 'users/password_reset_done.html',
        }, name='reset-password-done'),
    url(r'^users/reset-password/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/?$',
        'django.contrib.auth.views.password_reset_confirm',
        {
            'template_name': 'users/password_reset_confirm.html'
        }, name='reset-password-confirm'),
    url(r'^users/reset-password/done/?$',
        'django.contrib.auth.views.password_reset_complete',
        {
            'template_name': 'users/password_reset_complete.html'
        }, name='reset-password-complete'),

    (r'^users/', include('hackday.users.urls')),

    url(r'^rsvp/', 'hackday.messaging.views.rsvp', name='rsvp'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # django_qbe reporting
    url(r'^reporting/', include('django_qbe.urls')),

    # Arbitrary wiki pages FTW!
    url(r'^(?P<path>.*[^/])/?$', 'hackday.wiki.views.page', name='wiki-page'),

)


handler403 = 'hackday.common.forbidden'
handler404 = 'hackday.common.not_found'
handler500 = 'hackday.common.server_error'

