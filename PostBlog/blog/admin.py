from django.contrib import admin
from blog.models import Blog, Image, Comment

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Image)

