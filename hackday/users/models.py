from django.db import models


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

