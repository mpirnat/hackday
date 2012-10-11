from hackday.common import common_env
from hackday.charities.forms import SuggestCharityForm
from hackday.charities.models import Charity, STATUS
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.urlresolvers import reverse


def index(request):
    charities = Charity.objects.filter(status=STATUS.APPROVED).order_by("name")
    env = common_env()
    env['charities'] = charities
    return render(request, 'charities/index.html', env)


@login_required()
def suggest(request):
    error_message = None
    env = common_env()

    if request.method == 'POST':
        form = SuggestCharityForm(request.POST)
        if form.is_valid():
            try:
                charity = Charity(
                        name=form.cleaned_data['name'],
                        url=form.cleaned_data['url'],
                        description=form.cleaned_data['description'],
                        suggester=request.user,
                        status=STATUS.PENDING)
                charity.save()
            except IntegrityError:
                error_message = \
                        "That charity has already been suggested, thanks."
            else:
                return render(request, 'charities/suggest_done.html', env)
    else:
        form = SuggestCharityForm()

    env['form'] = form
    env['error_message'] = error_message
    return render(request, 'charities/suggest.html', env)
