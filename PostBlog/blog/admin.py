from django.contrib import admin
from blog.models import Blog, Image, Comment
from django.db.models.functions import Lower

# admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Image)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'pub_date', 'formset_image', 'user')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

    def get_ordering(self, request):
        return [Lower('user')]
