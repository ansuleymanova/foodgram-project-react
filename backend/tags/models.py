from django.db import models


class Tag(models.Model):
    id = models.IntegerField(primary_key=True,
                             editable=False)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200,
                             null=True,
                             unique=True)
    slug = models.SlugField(max_length=200,
                            unique=True,
                            null=True)
