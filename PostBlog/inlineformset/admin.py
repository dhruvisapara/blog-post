from django import forms
from django.contrib import admin

from inlineformset.models import Recipe, Ingredients


class RecipeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "Recipe: {}".format(obj.title)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ['name', 'recipe_name']
    search_fields = ("recipe__title",)

    def recipe_name(self, instance):
        return instance.recipe.title

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'recipe':
            return RecipeChoiceField(queryset=Recipe.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
