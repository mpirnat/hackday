import random

from hackday.messaging.models import Message, STATUS

def random_message(request):
    show = random.randint(0,5)
    message = None

    if show > 2:
        messages = Message.objects.filter(status=STATUS.ACTIVE).order_by('?')[:1]
        if messages:
            message = messages[0]


    return {'random_message': message}

