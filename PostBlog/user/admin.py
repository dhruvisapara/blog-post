from django.contrib import admin
from django.contrib.auth.models import Permission
from django.db.models.functions import Upper
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from user.models import User, Profile

admin.site.register(Profile)
admin.site.register(Permission)


def set_default_profile_picture(modeladmin, request, queryset):
    queryset.update(profile_image="images/blogger.png")


set_default_profile_picture.short_description = "Set profile picture for this users."


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'username', 'user_type', 'blog_display')
    list_filter = ("username",)
    ordering = ('profile_image',)
    editable_list = ['mobile_number']
    search_fields = ("username__startswith",)
    readonly_fields = ["dp_image", "profile_image"]
    actions = [
        set_default_profile_picture,
    ]

    def get_ordering(self, request):
        return [Upper('user_type')]

    def image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 45px; height:45px;" />'.format(obj.profile_image.url))
        return None

    def dp_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.profile_image.url,
            width=obj.profile_image.width,
            height=obj.profile_image.height,
        )
        )

    def blog_display(self, obj):
        if obj.blog.all():

            user_blog_list = ",\n ".join([
                child.title for child in obj.blog.all()
            ])
            return format_html('<h3 style="color:blue;" >{}</h3>&nbsp;'.format(user_blog_list))
        else:

            return format_html('<h3 style="color:red;" >Not Available</h3>')

    blog_display.short_description = "User's Blogs"
