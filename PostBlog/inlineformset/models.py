from datetime import datetime

from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    published = models.DateTimeField(default=datetime.now, null=True)
    description = models.TextField(blank=True, default=None)
    image = models.ImageField(upload_to='images', null=True, blank=True)


class Ingredients(models.Model):
    name = models.CharField(max_length=50)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
