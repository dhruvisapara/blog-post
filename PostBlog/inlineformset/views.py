from itertools import chain

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from inlineformset.forms import IngredientInlineFormset, RecipeForm
from inlineformset.models import Ingredients, Recipe


class RecipeView(CreateView):
    """This view should create recipes in inline formset."""
    form_class = RecipeForm
    template_name = "inline/recipe.html"

    def get_context_data(self, **kwargs):
        context = super(RecipeView, self).get_context_data(**kwargs)
        context['recipe_meta_formset'] = IngredientInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        """This method should create recipes and ingredients using inline formset."""
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        recipe_meta_formset = IngredientInlineFormset(self.request.POST, request.FILES)
        if form.is_valid() and recipe_meta_formset.is_valid():
            return self.form_valid(form, recipe_meta_formset)
        else:
            return self.form_invalid(form, recipe_meta_formset)

    def form_valid(self, form, recipe_meta_formset):
        self.object = form.save(commit=False)
        self.object.save()
        product_metas = recipe_meta_formset.save(commit=False)
        for meta in product_metas:
            meta.recipe = self.object
            meta.save()
        return redirect(reverse("blog:home"))

    def form_invalid(self, form, recipe_meta_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  recipe_meta_formset=recipe_meta_formset
                                  )
        )


class ShowRecipe(ListView):
    """Merge two queryset and return only one queryset."""
    template_name = 'inline/show_recipes.html'
    context_object_name = 'recipe_list'
    qs1 = Ingredients.objects.all()
    qs2 = Recipe.objects.all()
    queryset = list(chain(qs1, qs2))

    # def get_queryset(self):
    #     qs1 = Ingredients.objects.all()
    #     qs2 = Recipe.objects.all()
    #
    #     result = list(chain(qs1, qs2))
    #     return result


class RecipeUpdateView(UpdateView):
    model = Recipe
    success_url = reverse_lazy('blog:home')
    fields = '__all__'
    template_name = "inline/recipe_form.html"

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['inline_formset'] = IngredientInlineFormset(self.request.POST, instance=self.object)
            context['inline_formset'].full_clean()
        else:
            context['inline_formset'] = IngredientInlineFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['inline_formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)
