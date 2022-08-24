from django.forms import ModelForm, inlineformset_factory

from inlineformset.models import Recipe, Ingredients


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title','description','image']


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredients
        fields = "__all__"


IngredientInlineFormset = inlineformset_factory(Recipe, Ingredients, form=IngredientForm, extra=10,can_delete=True)
