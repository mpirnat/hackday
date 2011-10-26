from django.db import models


class STATUS(object):
    DRAFT = 'D'
    PUBLISHED = 'P'
    DELETED = 'X'

    CHOICES = (
        ('D', 'Draft'),
        ('P', 'Published'),
        ('X', 'Deleted'),
    )


class Page(models.Model):
    title = models.CharField('title of entry', max_length=255)
    slug = models.SlugField('slugified title', db_index=True, unique=True)
    content = models.TextField('page content')
    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)
    pub_date = models.DateTimeField('date published', null=True)

    def __unicode__(self):
        return self.title

    # TODO: models.ForeignKey on entry author
