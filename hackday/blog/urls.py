from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('blog.views',
    (r'^$', 'index'),
    (r'^(?P<entry_id>\d+)/*$', 'entry'),
    (r'^category/(?P<slug>[\w_-]+)/*$', 'category'),
    (r'^tag/(?P<slug>[\w_-]+)/*$', 'tag'),
    (r'^admin/*$', 'admin_blog_index'),
    (r'^admin/add/*$', 'admin_blog_edit'),
)
