from django.contrib.auth.models import User
from django.db import models
from assets.models import Attachment, ImageAttachment, Link


class STATUS(object):
    DRAFT = 'D'
    PUBLISHED = 'P'
    DELETED = 'X'

    CHOICES = (
        (DRAFT, 'Draft'),
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




class Page(models.Model):
    title = models.CharField('title of page', max_length=255)
    path = models.CharField('path of page', max_length=255, db_index=True,
            unique=True)
    content = models.TextField('page content')
    status = models.CharField(max_length=1, choices=STATUS.CHOICES)
    format = models.CharField(max_length=5, choices=FORMAT.CHOICES)
    navigable = models.BooleanField('in site navigation')
    order = models.IntegerField(null=True, blank=True)

    attachments = models.ManyToManyField(Attachment,
            related_name="%(app_label)s_%(class)s_attachments",
            blank=True)
    images = models.ManyToManyField(ImageAttachment,
            related_name="%(app_label)s_%(class)s_images",
            blank=True)
    links = models.ManyToManyField(Link,
            related_name="%(app_label)s_%(class)s_links",
            blank=True)

    author = models.ForeignKey(User)

    create_date = models.DateTimeField('date created', auto_now_add=True,
            editable=False)
    mod_date = models.DateTimeField('date modified', auto_now=True,
            editable=False)
    pub_date = models.DateTimeField('date published', null=True, blank=True)

    def __unicode__(self):
        return self.path
