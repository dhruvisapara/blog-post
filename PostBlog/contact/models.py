from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DataSet(models.Model):
    purpose = models.TextField()


class Measurement(models.Model):
    value = models.IntegerField()
    sets = models.ManyToManyField(DataSet,
                                  verbose_name="datasets this measurement appears in")
