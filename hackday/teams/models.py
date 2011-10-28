from django.db import models


class STATUS(object):
    ACTIVE = 'A'
    DISQUALIFIED = 'D'
    DELETED = 'X'

    CHOICES = (
        (ACTIVE, 'Active'),
        (DISQUALIFIED, 'Disqualified'),
        (DELETED, 'Deleted'),
    )


class Team(models.Model):
    name = models.CharField('name of team', max_length=255, db_index=True,
            unique=True)
    slug = models.SlugField('slugified team name', db_index=True, unique=True)
    project = models.TextField('description of project')

    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.name

    # TODO: FK to users for creator
    # TODO: FK to users for "captain"?
    # TODO: many-many to users for team members
    # TODO: FK to project category
    # TODO: FK to charity

