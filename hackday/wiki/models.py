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


class Page(models.Model):
    title = models.CharField('title of page', max_length=255)
    path = models.CharField('path of page', max_length=1024, db_index=True,
            unique=True)
    content = models.TextField('page content')
    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    attachments = models.ManyToManyField(Attachment,
            related_name="%(app_label)s_%(class)s_attachments")
    images = models.ManyToManyField(ImageAttachment,
            related_name="%(app_label)s_%(class)s_images")
    links = models.ManyToManyField(Link,
            related_name="%(app_label)s_%(class)s_links")

    author = models.ForeignKey(User)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)
    pub_date = models.DateTimeField('date published', null=True)

    def __unicode__(self):
        return self.path
