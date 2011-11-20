from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('users.views',
    (r'^/*$', 'index'),
    (r'^sign-up/*$', 'sign_up'),
    (r'^sign-in/*$', 'sign_in'),
    (r'^sign-out/*$', 'sign_out'),
    #(r'^(?P<username>\w+)/*$', 'profile'),
    #(r'^(?P<username>\w+)/edit/*$', 'edit_profile'),
)
