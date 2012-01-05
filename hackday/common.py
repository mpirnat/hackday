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


def forbidden(request):
    env = common_env()
    return render(request, '403.html', env)


def not_found(request):
    env = common_env()
    return render(request, '404.html', env)


def server_error(request):
    env = common_env()
    return render(request, '500.html', env)
