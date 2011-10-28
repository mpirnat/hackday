from django.db import models
from django.contrib.auth.models import User


class Tshirt(models.Model):

    description = models.CharField(max_length=50, unique=True)

    create_date = models.DateTimeField('date ceated', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.description


class Diet(models.Model):

    description = models.CharField(max_length=50, unique=True)

    create_date = models.DateTimeField('date ceated', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.description


class Location(models.Model):

    description = models.CharField(max_length=50, unique=True)

    create_date = models.DateTimeField('date ceated', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.description


class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)
    description = models.TextField('user bio')

    tshirt = models.ManyToManyField(Tshirt)
    diet = models.ManyToManyField(Diet)
    location = models.ManyToManyField(Location)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        if not hasattr(self, '_username'):
            self._username = User.objects.get(id=self.user_id).username
        return self._username

