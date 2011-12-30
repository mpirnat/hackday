from markdown import markdown
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from blog.models import Entry


class LatestEntriesFeed(Feed):
    title = "Hackday 2012"
    link = "/blog/"
    description = "A List of Wonderful Articles from Hackday 2012"

    feed_type = feedgenerator.Rss201rev2Feed

    def items(self):
        return Entry.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown(item.content, safe_mode="replace")

    def item_author_name(self, item):
        return item.author.username

    def item_categories(self, item):
        return str(item.tags)

    def item_pubdate(self, item):
        return item.pub_date

    

