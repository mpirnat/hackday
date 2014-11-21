from django.conf.urls.defaults import patterns, include, url
from hackday.blog.feeds import LatestEntriesFeed

urlpatterns = patterns('hackday.blog.views',
    url(r'^$', 'index', name='blog-index'),
    url(r'^(?P<entry_id>\d+)/*$', 'entry', name='blog-entry'),
    url(r'^(?P<entry_id>\d+)/email*$', 'email', name='blog-entry-email'),
    url(r'^category/(?P<slug>[\w_-]+)/*$', 'category', name='blog-category'),
    url(r'^tag/(?P<slug>[\w_-]+)/*$', 'tag', name='blog-tag'),
    url(r'^add/*$', 'blog_edit', name='blog-add'),
    url(r'^edit/(?P<entry_id>\d+)/*$', 'blog_edit', name='blog-edit'),
    url(r'^feed/$', LatestEntriesFeed(), name='blog-feed'),
)
