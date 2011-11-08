from django.db import models


class Link(models.Model):
    url = models.URLField('link url')
    title = models.CharField('link title', max_length=255)
    text = models.CharField('link text', max_length=255)
    
    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.url


class Attachment(models.Model):
    attached_file = models.FileField(upload_to='uploads/%Y/%m/%d')
    title = models.CharField('attachment title', max_length=255)
    alt_text = models.CharField('alt text', max_length=255)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.attached_file.url


class ImageAttachment(models.Model):
    attached_file = models.ImageField(upload_to='uploads/%Y/%m/%d',
            height_field='height', width_field='width')
    title = models.CharField('image title', max_length=255)
    alt_text = models.CharField('alt text', max_length=255)
    height = models.IntegerField('image height')
    width = models.IntegerField('image width')

    create_date = models.DateTimeField('date created', auto_now_add=True)
    mod_date = models.DateTimeField('date modified', auto_now=True)

    def __unicode__(self):
        return self.attached_file.url
