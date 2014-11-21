import tweepy
import HTMLParser

from django.conf import settings
from django.core.cache import cache

def tweets(request):
    if not hasattr(settings, 'TWITTER_CONSUMER_KEY'):
        return {'tweets': []};

    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                               settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                          settings.TWITTER_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    try:
        tweets = cache.get('hd_tweets')
        if not tweets:
            tweets = api.user_timeline()
            cache.set('hd_tweets', tweets, 60)

        tweets.sort(key=lambda x: x.created_at, reverse=True)

        # unsecape entities so django doesn't re-escape them
        # also expand link and media URLs
        parser = HTMLParser.HTMLParser()
        for tweet in tweets:
            tweet.text = parser.unescape(tweet.text)
            if tweet.retweeted:
                tweet.retweeted_status.text = parser.unescape(tweet.retweeted_status.text)
            for url in tweet.entities['urls']:
                tweet.text = tweet.text.replace(url['url'], url['expanded_url'])
            if 'media' in tweet.entities:
                for media in tweet.entities['media']:
                    tweet.text = tweet.text.replace(media['url'], media['expanded_url'])


    except Exception, e:
        tweets = []

    return {'tweets': tweets[:10]}

