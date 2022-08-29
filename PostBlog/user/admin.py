from django.contrib import admin
from django.contrib.auth.models import Permission
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.safestring import mark_safe

from user.models import User, Profile
from django.db.models.functions import Upper

admin.site.register(Profile)
admin.site.register(Permission)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type', 'blog_display')
    list_filter = ("username",)
    editable_list = ['mobile_number']
    search_fields = ("username__startswith",)
    readonly_fields = ["dp_image"]

    def get_ordering(self, request):
        return [Upper('user_type')]

    def dp_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.profile_image.url,
            width=obj.profile_image.width,
            height=obj.profile_image.height,
        )
        )

    def blog_display(self, obj):
        return ", ".join([
            child.title for child in obj.blog.all()
        ])

    blog_display.short_description = "User's Blogs"
