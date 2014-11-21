from django.shortcuts import render
from django.template import Context, loader

from hackday.common import common_env
from hackday.messaging.models import RSVP
from hackday.messaging.forms import RSVPForm

def rsvp(request):
    saved = False
    updated = False
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            will_attend = form.cleaned_data['will_attend']
            try:
                rsvp = RSVP.objects.get(email=email)
                updated = True
            except:
                rsvp = RSVP()
                saved = True
            rsvp.email = email
            rsvp.will_attend = will_attend
            rsvp.save()
    else:
        form = RSVPForm()

    env = common_env()
    env['form'] = form
    env['saved'] = saved
    env['updated'] = updated

    return render(request, "messaging/rsvp.html", env)
