from django.conf.urls.static import static
from django.urls import path

from PostBlog import settings
from inlineformset.views import RecipeView, ShowRecipe, RecipeUpdateView

app_name = "inline"
urlpatterns = [
                  path("", RecipeView.as_view(), name="create"),
                  path("list/", ShowRecipe.as_view(), name="recipe_list"),
                  path("<int:pk>/update/", RecipeUpdateView.as_view(), name="recipe-update"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
