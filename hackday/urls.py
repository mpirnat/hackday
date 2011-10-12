from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackday.views.home', name='home'),
    # url(r'^hackday/', include('hackday.foo.urls')),

    # Let the blog own the homepage?
    url(r'^/*$', 'blog.views.index'),

    url(r'^blog/*$', 'blog.views.index'),
    url(r'^blog/(?P<entry_id>\d+)/*$', 'blog.views.entry'),
    url(r'^blog/category/(?P<slug>[\w_-]+)/*$', 'blog.views.category'),
    url(r'^blog/tag/(?P<slug>[\w_-]+)/*$', 'blog.views.tag'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
