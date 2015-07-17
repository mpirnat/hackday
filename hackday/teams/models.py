import time

from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.template.defaultfilters import slugify

from hackday.assets.models import Attachment, ImageAttachment, Link
from hackday.charities.models import Charity
from hackday.voting.moremodels import Category


class STATUS(object):
    """
    Status of the team
    """
    ACTIVE = 'A'
    DISQUALIFIED = 'D'
    DELETED = 'X'

    CHOICES = (
        (ACTIVE, 'Active'),
        (DISQUALIFIED, 'Disqualified'),
        (DELETED, 'Deleted'),
    )


class PROJECT_TYPE(object):
    """
    Type of project -- 'implemented' (working code) or 'concept' (smoke and
    Powerpoint mirrors)
    """
    # I honestly came really close to calling these 'SMOKE' and 'MIRRORS' but
    # couldn't decide which to assign to which. - mpirnat
    IMPLEMENTED = 'I'
    CONCEPT = 'C'

    CHOICES = (
        (IMPLEMENTED, 'Implemented'),
        (CONCEPT, 'Non Implemented'),
    )


def create_unique_team_filename(instance, filename):
    """ Return a uniqque filename for an uploaded team file.
            -- called when saving a Team to the DB
    """
    filename_parts = filename.split('.')
    return 'teams/{team_slug}/{file_prefix}-{stamp}.{file_suffix}'.format(
            team_slug=instance.slug[:75],
            file_prefix='.'.join(filename_parts[:-1]),
            stamp=time.time(),
            file_suffix=filename_parts[-1])


class TeamCreateStatus(models.Model):
    """ A model to allow turning voting on and off on the site
        via the admin interface
    """
    online = models.BooleanField()

    def __unicode__(self):
        return self.online and "Online" or "Offline"

    class Meta:
        verbose_name_plural = "Team creation status"


class Team(models.Model):
    """
    A team of participants that will work on a project and compete for fabulous
    prizes, fame, and glory.

    Upon creation, a team needs:

        * a name--hopefully an awesome one
        * a slug, to be used for the URL of the team's page
        * a project description
        * a project type, so that we can differentiate "real" hacks vs. thought
          experiments (aka "code vs. ppt")
        * a creator
        * a captain
        * team members
        * a judged category
        * a charity that the team is supporting

    The creator and captain may have management powers above and beyond
    those of a mere member.
    """

    name = models.CharField('name of team', max_length=255, db_index=True,
            unique=True)
    slug = models.SlugField('slugified team name', db_index=True, unique=True,
            editable=False)

    project = models.TextField('description of project')
    logo = models.ImageField('team logo image', blank=True,
            upload_to=create_unique_team_filename)

    project_type = models.CharField('type of project', max_length=1,
            db_index=True, choices=PROJECT_TYPE.CHOICES)
    status = models.CharField(max_length=1, db_index=True,
            choices=STATUS.CHOICES)

    creator = models.ForeignKey(User,
            related_name="%(app_label)s_%(class)s_creator")
    captain = models.ForeignKey(User,
            related_name="%(app_label)s_%(class)s_captain")
    members = models.ManyToManyField(User,
            related_name="%(app_label)s_%(class)s_members")

    attachments = models.ManyToManyField(Attachment, blank=True,
            related_name="%(app_label)s_%(class)s_attachments")
    images = models.ManyToManyField(ImageAttachment, blank=True,
            related_name="%(app_label)s_%(class)s_images")
    links = models.ManyToManyField(Link, blank=True,
            related_name="%(app_label)s_%(class)s_links")

    category = models.ForeignKey(Category)
    charity = models.ForeignKey(Charity)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    @property
    def is_concept(self):
        return self.project_type == PROJECT_TYPE.CONCEPT

    @property
    def is_implemented(self):
        return self.project_type == PROJECT_TYPE.IMPLEMENTED

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  #TODO: check if slug exists in DB
        return super(Team, self).save()

    def add_captain_as_member(self):
        if not self.is_member(self.captain):
            self.members.add(self.captain)
            self.save()

    def is_member(self, user):
        return user in self.members.all()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
