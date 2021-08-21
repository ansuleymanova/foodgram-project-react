from django.db import models


class Ingredient(models.Model):
    id = models.IntegerField(primary_key=True,
                             editable=False)
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)
