from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('hackday.users.views',
    url(r'^/?$', 'index', name='users-home'),
    url(r'^sign-up/?$', 'sign_up', name='users-sign-up'),
    url(r'^sign-in/?$', 'sign_in', name='users-sign-in'),
    url(r'^sign-out/?$', 'sign_out', name='users-sign-out'),
    url(r'^view-profile/?$', 'profile_redirect', name='users-view-profile'),
    url(r'^edit-profile/?$', 'edit_profile_redirect', name='users-edit-profile-redirect'),
    url(r'^(?P<username>[\w,\.]+)/?$', 'profile', name='users-profile'),
    url(r'^(?P<username>[\w,\.]+)/edit/?$', 'edit_profile', name='users-edit-profile'),
)
