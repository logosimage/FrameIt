from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Blog(models.Model):
    title = models.CharField(max_length=255)

    content = models.TextField()
    author = models.ForeignKey(User)
    image = models.ImageField()


    slug = models.SlugField(null=True, blank=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs ):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Blog, self).save(*args, **kwargs)