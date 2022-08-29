from django.contrib import admin

from book.models import Book, TextBook, Author

admin.site.register(Book)


class TextBookAdminInline(admin.TabularInline):
    extra = 2
    model = TextBook


@admin.register(Author)
class AuthrModelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = (TextBookAdminInline,)
    fields = ('name',)


@admin.register(TextBook)
class TextBookModelAdmin(admin.ModelAdmin):
    list_display = ("title", "author_name")
    fields = ('author', 'title')

    def author_name(self, instance):
        return instance.author.name
