from django.db import models


STATUS_CHOICES = (
    ('D', 'Draft'),
    ('P', 'Published'),
    ('X', 'Deleted'),
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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)
    pub_date = models.DateTimeField('date published', null=True)

    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title

    # TODO: models.ForeignKey on entry author



