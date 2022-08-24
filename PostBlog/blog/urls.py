from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from blog.views import *

app_name = "blog"

urlpatterns = [
                  path("", BlogView.as_view(), name='home'),

                  path('blog_list/', AddBlogView.as_view(), name='add'),

                  path("userblog/", UserBlog.as_view(), name="userblog"),

                  path("update/<int:pk>/", UpdateBlog.as_view(), name="update"),

                  path("userblog/<int:pk>/", ImageView.as_view(), name="image"),

                  path("comment/<int:pk>/", AddComments.as_view(), name="comment"),

                  path("<int:comments>/", ShowComment.as_view(), name="display_comment"),

                  path("upload_image/", BlogImage.as_view(), name="upload_image"),

                  path("search/", SearchView.as_view(), name="search"),

                  path("detail/<int:pk>/", DetailBlogView.as_view(), name="detail"),

                  path("delete/<int:pk>/", BlogDelete.as_view(), name="delete"),

                  path("update_images/<int:pk>/", UpdateImage.as_view(), name="update_image"),

                  path("image_delete/<int:pk>/", ImageDelete.as_view(), name="delete_image"),
                  path("ajax/delete/", DeleteBlogAjax.as_view(), name="delete_blog_ajax"),
                  path("blog/userblog/ajax/update/", UpdateBlogAjax.as_view(), name="update_blog_ajax"),
                  path("formset/", BlogFormSetView.as_view(), name="formset"),
                  path("blog_formset/", update_blog_formset, name="blog_formset"),
                  path('form_image/',Image_request_form.as_view(),name="image-request"),
                  # path('random/',random,name='random')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
