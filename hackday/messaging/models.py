from django.contrib.auth.models import User
from django.db import models


class STATUS(object):
    # Using the same char values as blog posts & wiki pages for consistency, but
    # different verbose versions for clarity/semantic meaning.
    DRAFT = 'D'
    ACTIVE = 'A'
    DELETED = 'X'

    CHOICES = (
        (DRAFT, 'Draft'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    )


class Message(models.Model):
    description = models.TextField('message content')
    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    created_by = models.ForeignKey(User)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Messages"
        ordering = ['create_date']

class RSVP(models.Model):
    email = models.EmailField('email')
    will_attend = models.BooleanField('will attend')

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name_plural = "RSVPs"
        ordering = ['email']
