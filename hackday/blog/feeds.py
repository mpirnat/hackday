from markdown import markdown
from docutils.core import publish_parts
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from hackday.blog.models import Entry, FORMAT


class LatestEntriesFeed(Feed):
    title = "Hack Day Blog"
    link = "/blog/"
    description = "A list of the Hack Day blog entries"

    feed_type = feedgenerator.Rss201rev2Feed

    def items(self):
        return Entry.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if item.format == FORMAT.MARKDOWN:
            return markdown(item.content, safe_mode='remove')
        elif item.format == FORMAT.RESTRUCTURED_TEXT:
            parts = publish_parts(source=item.content, writer_name="html4css1")
            return parts['fragment']
        else:
            return item.content

    def item_author_name(self, item):
        return item.author.username

    def item_categories(self, item):
        return str(item.tags)

    def item_pubdate(self, item):
        return item.pub_date



