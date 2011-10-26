from wiki.models import Page, STATUS
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, loader


def page(request, path):
    page = get_object_or_404(Page, path=path, status=STATUS.PUBLISHED)

    t = loader.get_template('wiki/page.html')
    c = Context({
        'page': page,
    })

    return HttpResponse(t.render(c))
