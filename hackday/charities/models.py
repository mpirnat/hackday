from django.contrib.auth.models import User
from django.db import models
from hackday.assets.models import Attachment, ImageAttachment, Link


class STATUS(object):
    # Using the same char values as blog posts & wiki pages for consistency, but
    # different verbose versions for clarity/semantic meaning.
    PENDING = 'D'
    APPROVED = 'P'
    REJECTED = 'R'
    DELETED = 'X'

    CHOICES = (
        (PENDING, 'Pending Approval'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (DELETED, 'Deleted'),
    )


class Charity(models.Model):
    name = models.CharField('name of charity', max_length=255, db_index=True,
            unique=True)
    url = models.CharField('url', max_length=255)
    tax_id = models.CharField('tax id', max_length=10, blank=True, null=True)
    description = models.TextField('description of charity')
    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    attachments = models.ManyToManyField(Attachment,
            related_name="%(app_label)s_%(class)s_attachments", blank=True)
    images = models.ManyToManyField(ImageAttachment,
            related_name="%(app_label)s_%(class)s_images", blank=True)
    links = models.ManyToManyField(Link,
            related_name="%(app_label)s_%(class)s_links", blank=True)

    suggester = models.ForeignKey(User)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Charities"
        ordering = ['name']
