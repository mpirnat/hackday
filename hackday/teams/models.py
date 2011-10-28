from django.db import models
from charities.models import Charity
from django.contrib.auth.models import User


class STATUS(object):
    ACTIVE = 'A'
    DISQUALIFIED = 'D'
    DELETED = 'X'

    CHOICES = (
        (ACTIVE, 'Active'),
        (DISQUALIFIED, 'Disqualified'),
        (DELETED, 'Deleted'),
    )


class Category(models.Model):
    name = models.CharField('name of category', max_length=255, unique=True)
    slug = models.SlugField('slugified category name', db_index=True, unique=True)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.name


class Team(models.Model):
    name = models.CharField('name of team', max_length=255, db_index=True,
            unique=True)
    slug = models.SlugField('slugified team name', db_index=True, unique=True)
    project = models.TextField('description of project')

    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    creator = models.ForeignKey(User,
            related_name="%(app_label)s_%(class)s_creator")
    captain = models.ForeignKey(User,
            related_name="%(app_label)s_%(class)s_captain")
    members = models.ManyToManyField(User,
            related_name="%(app_label)s_%(class)s_members")

    project_category = models.ForeignKey(Category)
    charity = models.ForeignKey(Charity)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.name
