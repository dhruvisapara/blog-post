from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=20)


class Pizza(models.Model):
    name = models.CharField(max_length=20)
    toppings = models.ManyToManyField(Topping)
    is_soldout = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Available, 0->Soldout',
                                    choices=(
                                        (1, 'Available'), (0, 'Soldout')
                                    ))

