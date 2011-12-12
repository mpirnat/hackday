from django.contrib.auth.models import User
from django.db import models
from assets.models import Attachment, ImageAttachment, Link
from django.forms import ModelForm
from taggit.managers import TaggableManager


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


class Entry(models.Model):
    title = models.CharField('title of entry', max_length=255)
    slug = models.SlugField('slugified title', db_index=True,
            unique_for_date="pub_date")
    content = models.TextField('entry content')
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
    
    tags = TaggableManager(blank=True) 

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)
    pub_date = models.DateTimeField('date published', null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%d" % self.id 

class EntryForm(ModelForm):
    class Meta:
        model = Entry

