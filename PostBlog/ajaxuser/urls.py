from django.conf.urls.static import static
from django.urls import path

from PostBlog import settings
from ajaxuser import views

app_name="users"

urlpatterns = [
    path('crud/', views.CrudView.as_view(), name='crud_ajax'),
    path('crud/create/', views.CreateCrudUser.as_view(), name='crud_ajax_create'),
    path('crud/update/', views.UpdateCrudUser.as_view(), name='crud_ajax_update'),
    path('crud/delete/', views.DeleteCrudUser.as_view(), name='crud_ajax_delete'),
]

