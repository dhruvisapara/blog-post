from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=20)


class Pizza(models.Model):
    name = models.CharField(max_length=20)
    toppings = models.ManyToManyField(Topping)
