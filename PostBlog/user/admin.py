from django.contrib import admin
from django.contrib.auth.models import Permission
from user.models import User, Profile

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Permission)

