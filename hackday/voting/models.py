from django.db import models
from django.contrib.auth.models import User
from hackday.teams.models import Team
from hackday.voting.moremodels import Category


class STATUS(object):
    """
    Status values for a VoteCart.
    """
    ACTIVE = 'A'
    COMPLETED = 'C'

    CHOICES = (
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
    )


class VoteStatus(models.Model):
    """ A model to allow turning voting on and off on the site
        via the admin interface
    """
    online = models.BooleanField()

    def __unicode__(self):
        return self.online and "Online" or "Offline"

    class Meta:
        verbose_name_plural = "Voting status"

class VoteMessage(models.Model):
    """ A model to keep track of processed email/sms vote messages """

    message_id = models.CharField(max_length=255)

    def __unicode__(self):
        return self.message_id

class VoteCart(models.Model):
    """
    A 'shopping cart' for votes; lets us gather up all of a user's votes,
    and redisplay them for confirmation/correction.

    Once a VoteCart has been completed, its corresponding Votes should be
    disconnected from the VoteCart to preserve the anonymity of the voting.

    The presence of a VoteCart for the user will serve as an indicator that
    they have either started voting or completed voting (in which case, they
    can't vote again, thankyouverymuch).
    """

    user = models.ForeignKey(User)
    status = models.CharField(max_length=1, choices=STATUS.CHOICES)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)


class Vote(models.Model):
    """
    Vote for Pedro!

    An individual vote for a team in a category.

    Once voting is completed, the cart relationship should be nulled out so
    that votes are anonymous once cast.
    """

    team = models.ForeignKey(Team)
    category = models.ForeignKey(Category)
    cart = models.ForeignKey(VoteCart, null=True)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mode_date = models.DateTimeField('date modified', auto_now=True)
