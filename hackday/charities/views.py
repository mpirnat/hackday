from charities.models import Charity, STATUS
from django.http import HttpResponse
from django.template import Context, loader


def index(request):
    charities = Charity.objects.filter(status=STATUS.APPROVED).order_by("name")

    t = loader.get_template('charities/index.html')
    c = Context({
        'charities': charities,
    })

    return HttpResponse(t.render(c))
