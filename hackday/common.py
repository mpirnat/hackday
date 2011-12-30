from wiki.models import Page

def get_nav_pages():
    pages = Page.objects.filter(navigable=True).order_by('order', 'title')
    return pages


def common_env():
    env = {
        'nav_pages': get_nav_pages(),
    }
    return env
