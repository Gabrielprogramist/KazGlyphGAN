# image_processing/models.py

from django.db import models

class Publication(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    abstract = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title
