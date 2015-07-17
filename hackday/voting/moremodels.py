"""
Extra models for the voting app.  We'd like to keep them in the main
voting.models module, but can't due to the circular import problems that can
arise.
"""
from django.db import models

class TYPE(object):
    """
    Differentiate categories by type; some categories may be decided by
    a panel of judges, while others may be voted on by event participants.
    """
    JUDGED = 'J'
    VOTED = 'V'

    CHOICES = (
        (JUDGED, 'Judged'),
        (VOTED, 'Voted'),
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


class Category(models.Model):
    """
    Awards categories that teams can compete for.

    Categories of 'voted' type should be available for popular voting in the
    voting UI.

    Categories of 'judged' type should NOT be available for popular voting as
    they will be decided by a panel of judges outside of the voting system.

    Teams should self-declare a 'judged' category to enter when the team is
    created.
    """

    name = models.CharField('name of category', max_length=255, unique=True)
    slug = models.SlugField('slugified category name', db_index=True,
            unique=True)
    description = models.TextField('description of category')
    type = models.CharField('type of category', max_length=1, db_index=True,
            choices=TYPE.CHOICES)
    project_type = models.CharField('type of project', max_length=1,
                choices=PROJECT_TYPE.CHOICES, blank=True)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.name

    @property
    def is_concept(self):
        return self.project_type is not None and self.project_type == PROJECT_TYPE.CONCEPT

    @property
    def is_implemented(self):
        return self.project_type is not None and self.project_type == PROJECT_TYPE.IMPLEMENTED

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
