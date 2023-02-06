from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

import string
import random


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField(default='default.jpg')
    added_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)

    def get_unique_slug(self):
        unique_slug = slugify(self.title)
        counter = 1
        while self.__class__.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slugify(self.title)}-{random_string_generator()}{counter}'
            counter += 1
        return unique_slug


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    added_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


def random_string_generator(size=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join([random.choice(chars) for _ in range(size)])
