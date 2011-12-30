from common import common_env
from blog.models import Entry, EntryForm, STATUS
from django.http import HttpResponse
from django.template import Context, loader
from django.forms.models import modelformset_factory
from django.core.context_processors import csrf
from django.shortcuts import render
from django.template import RequestContext


def index(request):
    latest_entries = Entry.objects.filter(status=STATUS.PUBLISHED).\
            order_by('-pub_date')[:5]
    env = common_env()
    env['latest_entries'] = latest_entries
    return render(request, 'blog/index.html', env)


def entry(request, entry_id):
    entry = Entry.objects.get(pk=entry_id, status=STATUS.PUBLISHED)
    env = common_env()
    env['entry'] = entry
    return render(request, 'blog/entry.html', env)


def category(request, slug):
    entries = Entry.objects.filter(categories__slug=slug,
            status=STATUS.PUBLISHED).order_by('pub_date')
    env = common_env()
    env['entries'] = entries
    env['slug'] = slug
    return render(request, 'blog/category.html', env)


def tag(request, slug):
    entries = Entry.objects.filter(tags__slug=slug,
            status=STATUS.PUBLISHED).order_by('pub_date')
    env = common_env()
    env['entries'] = entries
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


