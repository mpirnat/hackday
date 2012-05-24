import json

from urllib2 import urlopen, Request, HTTPError
from urllib import quote
from django.contrib.sites.models import Site
from django.shortcuts import render
from wiki.models import Page, STATUS

def get_nav_pages():
    pages = Page.objects.filter(status=STATUS.PUBLISHED, navigable=True).order_by('order', 'title')
    return pages


def common_env():
    env = {
        'nav_pages': get_nav_pages(),
    }
    return env


def common_env_processor(request):
        return common_env()


def forbidden(request):
    env = common_env()
    return render(request, '403.html', env)


def not_found(request):
    env = common_env()
    return render(request, '404.html', env)


def server_error(request):
    env = common_env()
    return render(request, '500.html', env)


def get_short_url(path):
    if not path.startswith("/"):
        path = "/{0}".format(path)
    domain = Site.objects.get_current().domain

    if not domain.startswith('http://'):
        domain = "http://{0}".format(domain)

    url = "{0}{1}".format(domain, path)

    try:
        e = urlopen(Request('http://goo.gl/api/url','url=%s'%quote(url),
                        {'User-Agent':'toolbar'}))
        data  = json.loads(e.read())
        if 'short_url' not in data:
            return url
        else:
            return data['short_url']
    except Exception, e:
        return url
