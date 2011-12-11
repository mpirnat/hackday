from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('blog.views',
    (r'^$', 'index'),
    (r'^(?P<entry_id>\d+)/*$', 'entry'),
    (r'^category/(?P<slug>[\w_-]+)/*$', 'category'),
    (r'^tag/(?P<slug>[\w_-]+)/*$', 'tag'),
    (r'^add/*$', 'blog_edit'),
    (r'^/edit/(?P<entry_id>\d+)$', 'blog_edit'),
)
