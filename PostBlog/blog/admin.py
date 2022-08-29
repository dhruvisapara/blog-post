from django import forms
from django.contrib import admin
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from blog.models import Blog, Comment, Image


def change_rating_to_Excellent(modeladmin, request, queryset):
    queryset.update(rating="e")


def change_rating_to_Bad(modeladmin, request, queryset):
    queryset.update(rating="b")


def change_rating_to_Average(modeladmin, request, queryset):
    queryset.update(rating="a")


change_rating_to_Excellent.short_description = "Mark Selected Products as Excellent."
change_rating_to_Bad.short_description = "Mark Selected Products as Bad."
change_rating_to_Average.short_description = "Mark Selected Products as Average."


class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"

    def clean_title(self):
        name = self.cleaned_data["title"]
        if Blog.objects.filter(title=name).exists():
            raise forms.ValidationError(
                f"{name} is already exist ,please change your blog title."
            )

        return self.cleaned_data["title"]


@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin):
    form = BlogAdminForm
    list_display = (
        "title",
        "active",
        "pub_date",
        "user",
        "profile_according_to_user",
        "is_user_is_staff",
        "rating",
        'Comment_according_to_blog'

    )
    list_filter = ("pub_date", "user")
    exclude = ("user",)
    date_hierarchy = "pub_date"

    list_editable = ("rating",)
    search_fields = ("title__startswith",)
    actions = [
        change_rating_to_Excellent,
        change_rating_to_Bad,
        change_rating_to_Average,
    ]

    def profile_according_to_user(self, obj):
        return format_html(
            '<a class="button"  href="/admin/user/user/{}/change/">Profile</a>&nbsp;'.format(obj.user.pk)
        )

    profile_according_to_user.short_description = 'Customer Profile'

    def Comment_according_to_blog(self, obj):
        return format_html(
            '<a class="button"  href="/blog/{}/">Comment</a>&nbsp;'.format(obj.id)
        )

    Comment_according_to_blog.short_description = 'Blog Comments'

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

    def get_ordering(self, request):
        return [Lower("user")]

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        if not change:
            obj.user = request.user
        return obj

    def is_user_is_staff(self, obj):
        return obj.user.user_type == "staff"

    is_user_is_staff.boolean = True


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_filter = ["blog"]

    def has_add_permission(self, request):
        return False


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
