import tweepy

from common import common_env
from users.models import User, UserProfile
from django.core.mail import send_mass_mail
from django.conf import settings
from django.template import loader, Context
from django.contrib.sites.models import Site

class BlogNotification(object):

    def __init__(self, entry):
        self.entry = entry
        self.site = Site.objects.get_current()
        self.context = {'entry': self.entry,
                        'site_domain': self.get_site_domain(),
                        'site_name': self.site.name}

    def send_email(self):
        profiles = UserProfile.objects.filter(notify_by_email=True)
        recipients = [p.user.email for p in profiles]

        subject = '[{0}]: {1}'.format(self.site.name, self.entry.title)
        body = self.render_template('blog/notification_email.html')
        messages = []
        for recipient in recipients:
            messages.append((subject, body, settings.DEFAULT_FROM_EMAIL,
                             [recipient]))

        send_mass_mail(messages, fail_silently=True)

    def send_tweet(self):
        if not hasattr(settings, 'TWITTER_CONSUMER_KEY'):
            return;

        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                                   settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                              settings.TWITTER_ACCESS_TOKEN_SECRET)

        update = self.render_template('blog/notification_tweet.html')
        api = tweepy.API(auth)
        try:
            api.update_status(update)
        except tweepy.TweepError:
            pass # avoid errors from duplicate posts during testing


    def render_template(self, template):
        t = loader.get_template(template)
        return t.render(Context(self.context))

    def get_site_domain(self):
        if not self.site.domain.startswith('http'):
            return 'http://{0}'.format(self.site.domain)
        else:
            return self.site.domain

