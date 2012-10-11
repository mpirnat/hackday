from django.conf.urls.defaults import patterns, url

from hackday.teams.models import Team, STATUS
from hackday.teams.views import delete
from hackday.teams.views import upload_attachment, remove_attachment
from hackday.teams.views import upload_image, remove_image
from hackday.teams.views import add_link, remove_link
from hackday.teams.views import TeamCreateView
from hackday.teams.views import TeamDetailView
from hackday.teams.views import TeamListView
from hackday.teams.views import TeamUpdateView


urlpatterns = patterns('hackday.teams.views',
    url(r'^/?$', TeamListView.as_view(), name='teams-list'),
    url(r'^create/?$', TeamCreateView.as_view(), name='teams-create'),
    url(r'^edit/(?P<slug>[\w-]+)/*$', TeamUpdateView.as_view(),
        name='teams-edit'),
    url(r'^(?P<slug>[\w-]+)/*$', TeamDetailView.as_view(),
        name='teams-detail'),
    url(r'^delete/(?P<slug>[\w-]+)/*$', delete, name='teams-delete'),
    url(r'^upload-attachment/(?P<slug>[\w-]+)$',
        upload_attachment,
        name='teams-upload-attachment'),
    url(r'^delete-attachment/(?P<slug>[\w-]+)/(?P<attachment_id>[\d]+)$',
        remove_attachment,
        name='teams-remove-attachment'),
    url(r'^upload-image/(?P<slug>[\w-]+)$',
        upload_image,
        name='teams-upload-image'),
    url(r'^delete-image/(?P<slug>[\w-]+)/(?P<attachment_id>[\d]+)$',
        remove_image,
        name='teams-remove-image'),
    url(r'^add-link/(?P<slug>[\w-]+)$',
        add_link,
        name='teams-add-link'),
    url(r'^delete-link/(?P<slug>[\w-]+)/(?P<attachment_id>[\d]+)$',
        remove_link,
        name='teams-remove-link'),
)
