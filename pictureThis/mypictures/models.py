from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime


def upload_handler(instance, filename):
    return "{date}/{file}".format(date=datetime.date.today(), file=filename)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True)
    image = models.ForeignKey('Image', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)

    def __str__(self):
        return self.title

    def display_tags(self):
        return ', '.join([tag.name for tag in self.tags.all()])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Blog, self).save(*args, **kwargs)


class Image(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to=upload_handler)
    alt = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
