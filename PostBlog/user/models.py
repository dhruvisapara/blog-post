import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import Token

from PostBlog import settings

MALE = "male"
GENDER = (
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other'),

)
MANAGER = "manager"
STAFF = "staff"
AUTHOR = "author"
USER_CHOICES = ((MANAGER, 'manager'), (STAFF, 'staff'), (AUTHOR, 'author'))


class User(AbstractUser):
    """This model includes all the information related to user """
    username_validator = UnicodeUsernameValidator()
    mobile_number = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    Gender = models.CharField(choices=GENDER, blank=True, max_length=30),
    age = models.IntegerField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='images', default=None, blank=True, null=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(default=AUTHOR, choices=USER_CHOICES, max_length=8)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    def __repr__(self):
        return self.username

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')


class Profile(models.Model):
    """to generate particular user's profile add onetoone field so each user has its own profile"""
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
