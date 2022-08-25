from django.contrib import admin
from django.contrib.auth.models import Permission
from user.models import User, Profile
from django.db.models.functions import Upper

admin.site.register(Profile)
admin.site.register(Permission)


@admin.register(User)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('username', 'Gender', 'user_type')
    list_filter = ("username",)
    editable_list = ['mobile_number']
    search_fields = ("username__startswith",)

    def get_ordering(self, request):
        return [Upper('user_type')]
