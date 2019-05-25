from django.db import models
from tagging.models import TaggedItem


class Author(models.Model):
    first_name = models.CharField(
        max_length=32,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        max_length=64,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Book(models.Model):
    title = models.CharField(
        max_length=256,
        null=False,
        blank=False
    )
    author = models.ManyToManyField(
        'Author',
        related_name='books',
    )
    summary = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
