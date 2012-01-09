import tweepy
import os

from BeautifulSoup import BeautifulSoup
from email.MIMEImage import MIMEImage
from common import common_env
from users.models import User, UserProfile
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader, Context
from django.contrib.sites.models import Site

class BlogNotification(object):

    def __init__(self, entry):
        self.entry = entry
        self.site = Site.objects.get_current()
        self.context = {'entry': self.entry,
                        'STATIC_URL':settings.STATIC_URL,
                        'site_domain': self.get_site_domain(),
                        'site_name': self.site.name}

    def send_email(self):
        project_path = os.path.dirname(os.path.normpath(os.sys.modules[settings.SETTINGS_MODULE].__file__))
        profiles = UserProfile.objects.filter(notify_by_email=True)
        recipients = [p.user.email for p in profiles]

        subject = '[{0}]: {1}'.format(self.site.name, self.entry.title)
        body = self.render_template('blog/notification_email.html')
        message = EmailMultiAlternatives(subject,
                                         body,
                                         settings.DEFAULT_FROM_EMAIL,
                                         [settings.DEFAULT_FROM_EMAIL],
                                         recipients)
        try:
            body_html = self.render_template('blog/notification_email_html.html')

            soup = BeautifulSoup(body_html)
            images = {}
            for index, tag in enumerate(soup.findAll(self._image_finder)):
                if tag['src'] not in images.keys():
                    images[tag['src']] = "image_{0}".format(index)
                tag['src'] = 'cid:{0}'.format(images[tag['src']])

            body_html = str(soup)

            for filename, file_id in images.items():
                image_file = open(project_path + filename, 'rb')
                msg_image = MIMEImage(image_file.read())
                image_file.close()
                msg_image.add_header('Content-ID', '<{0}>'.format(file_id))
                message.attach(msg_image)

            message.attach_alternative(body_html, "text/html")

        except Exception, e:
            # if we can't load the html template or related images,
            # don't send the HTML version
            pass

        message.send()

    def _image_finder(self, tag):
        return (tag.name == u'img')

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

