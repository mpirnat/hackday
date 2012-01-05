from common import common_env
from blog.models import Entry, EntryForm, STATUS
from django.http import HttpResponse
from django.template import Context, loader
from django.forms.models import modelformset_factory
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.template import RequestContext


def _get_paginated_entries(all_entries, page, page_size):
    paginator = Paginator(all_entries, page_size)

    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    return entries


def index(request):
    all_entries = Entry.objects.filter(status=STATUS.PUBLISHED).\
            order_by('-pub_date')
    page = request.GET.get('page', 1)

    env = common_env()
    env['entries'] = _get_paginated_entries(all_entries, page, 5)
    return render(request, 'blog/index.html', env)


def entry(request, entry_id):
    if request.user.is_superuser:
        entry = Entry.objects.get(pk=entry_id)
    else:
        entry = Entry.objects.get(pk=entry_id, status=STATUS.PUBLISHED)
    env = common_env()
    env['entry'] = entry
    return render(request, 'blog/entry.html', env)


def category(request, slug):
    all_entries = Entry.objects.filter(categories__slug=slug,
            status=STATUS.PUBLISHED).order_by('-pub_date')
    page = request.GET.get('page', 1)

    env = common_env()
    env['entries'] = _get_paginated_entries(all_entries, page, 10)
    env['slug'] = slug
    return render(request, 'blog/category.html', env)


def tag(request, slug):
    all_entries = Entry.objects.filter(tags__slug=slug,
            status=STATUS.PUBLISHED).order_by('-pub_date')
    page = request.GET.get('page', 1)

    env = common_env()
    env['entries'] = _get_paginated_entries(all_entries, page, 10)
    env['slug'] = slug
    return render(request, 'blog/tag.html', env)


def blog_edit(request, entry_id=None):
    entry_formset = EntryForm()
    errors = None

    if request.method == 'GET':
        entry_form = EntryForm()
        if entry_id:
            entry_formset = EntryForm(instance=Entry.objects.get(pk=entry_id))

    if request.method == 'POST':
        formset = EntryForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            entry_formset = "Entry Saved" # do something.
        else:
            errors = str(formset.errors)

    t = loader.get_template('blog/admin_edit.html')
    c = RequestContext(request, {
        'entry_formset': entry_formset,
        'errors' : errors,
    })

    return HttpResponse(t.render(c))


