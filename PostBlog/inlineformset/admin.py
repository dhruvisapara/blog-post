from django.contrib import admin

from inlineformset.models import Recipe, Ingredients

admin.site.register(Recipe)
admin.site.register(Ingredients)