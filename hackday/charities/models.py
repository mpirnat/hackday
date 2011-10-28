from django.db import models


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
    tax_id = models.CharField('tax id', max_length=10)
    description = models.TextField('description of charity')
    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.name

    # TODO: models.ForeignKey on user who suggested charity?
