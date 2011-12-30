from common import common_env
from charities.models import Charity, STATUS
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader


def index(request):
    charities = Charity.objects.filter(status=STATUS.APPROVED).order_by("name")
    env = common_env()
    env['charities'] = charities
    return render(request, 'charities/index.html', env)
