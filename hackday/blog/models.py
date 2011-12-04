from django.contrib.auth.models import User
from django.db import models
from assets.models import Attachment, ImageAttachment, Link
from django.forms import ModelForm

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


class Category(models.Model):
    slug = models.SlugField('category slug', unique=True, db_index=True)
    name = models.CharField('category name', max_length=50)
    create_date = models.DateTimeField('date created', auto_now_add=True)

    def __unicode__(self):
        return self.name


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
    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

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
        return self.title

class EntryForm(ModelForm):
    class Meta:
        model = Entry

