from hackday.common import common_env
from hackday.wiki.models import Page, STATUS
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader


def page(request, path):
    if request.user.has_perms('wiki.add_page'):
        page = get_object_or_404(Page, path=path)
    else:
        page = get_object_or_404(Page, path=path, status=STATUS.PUBLISHED)
    env = common_env()
    env['page'] = page
    return render(request, 'wiki/page.html', env)
