#!/usr/bin/env python
import re
import imaplib
import getopt, getpass
import email, email.Errors, email.Header, email.Message, email.Utils

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.core.mail import send_mail
from hackday.teams.models import Team, STATUS
from hackday.users.models import UserProfile
from hackday.voting.moremodels import Category, TYPE
from hackday.voting.models import VoteCart, VoteMessage, VoteStatus, STATUS
from hackday.voting.views import _insert_or_update_vote


PATTERN = re.compile(r'^.*Content-class', re.MULTILINE)
VOTE_PATTERN = re.compile(r'\d+-\d+', re.MULTILINE)
EMAIL_PATTERN = re.compile(r'\S+@\S+')
PHONE_PATTERN = re.compile(r'[\(]{0,1}\d{3}[\)]{0,1}[\s*,-]{0,1}\d{3}[-,]\d{4}',
                           re.MULTILINE)

us_phone = USPhoneNumberField()

def get_user(sender):
    """ given an email address or phone, return the first user whose
        main email, alternate email, or phone number matches (in that order)
    """

    for phone in PHONE_PATTERN.findall(sender):
        try:
            phone = us_phone.clean(phone)
            profile = UserProfile.objects.filter(phone=phone)[0]
            return profile.user
        except:
            pass

    for email in EMAIL_PATTERN.findall(sender):
        email = email.lstrip('<').rstrip('>')
        try:
            return User.objects.filter(email=email)[0]
        except:
            try:
                profile = UserProfile.objects.filter(alternate_email=email)[0]
                return profile.user
            except:
                pass

    return None


def get_cart(sender):
    user = get_user(sender)
    if not user:
        return None

    try:
        cart = VoteCart.objects.get(user=user.id)
    except:
        cart = VoteCart(user=user, status=STATUS.ACTIVE)
        cart.save()
    return cart


def process_message(text, msgnum):
    # found some messages with odd characters before the Content-class declaration
    # get rid of those here
    text = PATTERN.sub('Content-class', text)
    try:
        msg = email.message_from_string(text)
    except email.Errors.MessageError, val:
        warn("Message %s parse error: %s" % (msgnum, str(val)))
        return text

    return msg


def read_inbox():
    votes = []
    try:
        mbox = imaplib.IMAP4_SSL(settings.VOTE_EMAIL_SERVER,
                                 settings.VOTE_EMAIL_PORT)
    except:
        return -1
    mbox.login(settings.VOTE_EMAIL_USER, settings.VOTE_EMAIL_PASSWORD)

    mbox.select('Inbox')
    typ, dat = mbox.search(None, '(UNDELETED)')

    for num in dat[0].split():
        typ, dat = mbox.fetch(num, '(RFC822)')
        if typ != 'OK':
		    pass
        message = dat[0][1]
	votes.append(process_message(message, num))
    mbox.close()

    return votes


def parse_votes(message):
    votes = []
    if message.is_multipart():
        sub_messages = message.get_payload()
        for sub_message in sub_messages:
            votes.extend(parse_votes(sub_message))
    else:
        votes = VOTE_PATTERN.findall(message.get_payload(decode=True))
    return list(set(votes))


def process_votes(message, cart):
    votes = parse_votes(message)
    results = []
    errors = []
    for vote in votes:
        category_id, team_id = vote.split('-')
        try:
            category = Category.objects.get(id=category_id, type=TYPE.VOTED)
            team = Team.objects.get(id=team_id, status=STATUS.ACTIVE)
            _insert_or_update_vote(cart, category, team)
            results.append("{0} - {1}".format(category.name, team.name))
        except:
            errors.append("invalid vote {0}-{1}".format(
                category_id, team_id))

    send_response(message, results, errors)


def send_response(message, results, errors):
    if results:
        body = "Votes: \n{0}".format(",\n".join(results))
        email_response(body, message)

    if errors:
        body = "Errors: {0}".format(",\n".join(errors))
        email_response(body, message)

    if not errors and not results:
        body = 'Error: no valid votes found.'
        email_response(body, message)


def email_response(body, message):
    send_mail('HackDay Voting',
               body,
               settings.VOTE_EMAIL_ADDRESS,
               [message.get('From')],
               fail_silently=False)


def main():

    try:
        online = VoteStatus.objects.all()[0].online
    except:
        online = False

    messages = read_inbox()
    for message in messages:
        message_id = message.get('Message-ID')
        try:
            processed = VoteMessage.objects.get(message_id=message_id)
        except:
            cart = get_cart(message.get('From'))
            if cart is None:
                send_response(message, [], ["Sorry we couldn't find your account."])
            elif cart and not online:
                send_response(message, [], ["We found you, but voting is currently offline.  Try again later!"])
            else:
                process_votes(message, cart)

            processed = VoteMessage(message_id=message_id)
            processed.save()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
