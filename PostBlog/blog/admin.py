from django import forms
from django.contrib import admin
from django.db.models.functions import Lower

from blog.models import Blog, Comment, Image

admin.site.site_header = 'Blog-Post admin'
admin.site.site_title = 'Blog-Post admin'
admin.site.index_title = 'Blog administration'
admin.site.site_url = 'http://127.0.0.1:8000/blog/'


def change_rating_to_Excellent(modeladmin, request, queryset):
    queryset.update(rating='e')


def change_rating_to_Bad(modeladmin, request, queryset):
    queryset.update(rating='b')


def change_rating_to_Average(modeladmin, request, queryset):
    queryset.update(rating='a')


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
            raise forms.ValidationError(f"{name} is already exist ,please change your blog title.")

        return self.cleaned_data["title"]


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('title', 'active', 'pub_date', 'formset_image', 'user', 'rating')
    list_filter = ("pub_date",)
    list_editable = ('rating',)
    search_fields = ("title__startswith",)
    actions = [change_rating_to_Excellent, change_rating_to_Bad, change_rating_to_Average]

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

    def get_ordering(self, request):

        return [Lower('user')]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
