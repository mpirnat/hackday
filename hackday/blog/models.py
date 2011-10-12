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


class Tag(models.Model):
    slug = models.SlugField('tag slug', unique=True, db_index=True)
    name = models.CharField('tag name', max_length=50)
    create_date = models.DateTimeField('date created', auto_now_add=True)


class Post(models.Model):
    title = models.CharField('title of post', max_length=200)
    slug = models.SlugField('slugified title', db_index=True,
            unique_for_date="pub_date")
    content = models.TextField('post content')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    pub_date = models.DateTimeField('date published')
    edit_date = models.DateTimeField('date edited', auto_now=True)

    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

    # TODO: models.ForeignKey on post author



