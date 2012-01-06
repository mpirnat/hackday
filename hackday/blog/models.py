from common import get_short_url
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from assets.models import Attachment, ImageAttachment, Link
from django.forms import ModelForm
from taggit.managers import TaggableManager
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from blog.notifications import BlogNotification

ENTRY_STATUS = {}

class STATUS(object):
    DRAFT = 'D'
    PUBLISHED = 'P'
    REVIEW = 'R'
    DELETED = 'X'

    CHOICES = (
        (DRAFT, 'Draft'),
        (REVIEW, 'Review'),
        (PUBLISHED, 'Published'),
        (DELETED, 'Deleted'),
    )


class FORMAT(object):
    HTML = 'H'
    MARKDOWN = 'MD'
    RESTRUCTURED_TEXT = 'RST'

    CHOICES = (
        (MARKDOWN, 'Markdown'),
    #    (RESTRUCTURED_TEXT, 'Restructured Text'),
    #    (HTML, 'HTML'),
    )


class Category(models.Model):
    slug = models.SlugField('category slug', unique=True, db_index=True)
    name = models.CharField('category  name', max_length=50)
    create_date = models.DateTimeField('date created', auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    slug = models.SlugField('tag slug', unique=True, db_index=True)
    name = models.CharField('tag name', max_length=50)
    create_date = models.DateTimeField('date created', auto_now_add=True)

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    title = models.CharField('title of entry', max_length=255)
    slug = models.SlugField('slugified title', db_index=True,
            unique_for_date="pub_date")
    content = models.TextField('entry content')
    format = models.CharField(max_length=5, choices=FORMAT.CHOICES)
    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    attachments = models.ManyToManyField(Attachment,
            related_name="%(app_label)s_%(class)s_attachments", \
            blank=True)
    images = models.ManyToManyField(ImageAttachment,
            related_name="%(app_label)s_%(class)s_images", \
            blank=True)
    links = models.ManyToManyField(Link,
            related_name="%(app_label)s_%(class)s_links", \
            blank=True)

    author = models.ForeignKey(User)

    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    create_date = models.DateTimeField('date created', auto_now_add=True,
            editable=False)
    mod_date = models.DateTimeField('date modified', auto_now=True,
            editable=False)
    pub_date = models.DateTimeField('date published', null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-entry', args=[self.id])

    def short_url(self):
        return get_short_url(self.get_absolute_url())

    class Meta:
        verbose_name_plural = "Entries"


class EntryForm(ModelForm):

    class Meta:
        model = Entry


@receiver(pre_save, sender=Entry)
def blog_entry_will_save(sender, instance, raw, **kwargs):
    if instance.id:
        db_data = Entry.objects.get(pk=instance.id)
        ENTRY_STATUS[instance.id] = db_data.status

@receiver(post_save, sender=Entry)
def blog_entry_did_save(sender, instance, created, raw, **kwargs):
    is_published = instance.status == STATUS.PUBLISHED
    was_published = ENTRY_STATUS.get(instance.id) == STATUS.PUBLISHED

    if is_published and not was_published:
        notifier = BlogNotification(instance)
        notifier.send_email()
        notifier.send_tweet()
