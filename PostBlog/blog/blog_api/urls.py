from django.urls import path, include
from rest_framework import routers

from blog.blog_api.views import *

app_name = "blog_api"
router = routers.SimpleRouter()
router.register(r'blogs', BlogViewSet, basename="blogs")
router.register(r'comment-set', CommentViewSet, basename="comments")
router.register(r'image-set', ImageViewSet, basename="image")
router.register(r'user-blog', UserBlogViewSet, basename="user-blog")

urlpatterns = [
    path('', include(router.urls)),

    # path("", BlogListApiView.as_view(), name="home"),
    # path("blog-date/", DateList.as_view(), name="blog-date"),
    # path('blog-add/', AddBlogApiView.as_view(), name='add'),
    # path("userblog/", UserBlogApiview.as_view(), name='userblog'),
    # path("comment-set/<int:pk>/comment/",CommentViewSet.as_view({'post'}),name='comment')

    # path("update/<int:pk>/", UpdateBlogApiView.as_view(), name="update"),
    #
    # path("userblog/<int:pk>/", ImageApiView.as_view(), name="upload_image"),
    #
    # path("comment/<int:pk>/", AddCommentsApiView.as_view(), name="comment"),
    #
    # path('<int:pk>/', DisplayCommentApiView.as_view(), name='display_comment'),
    #
    # path("upload_image/<int:pk>/", BlogUploadImageApiView.as_view(), name="upload_image"),
    #
    # # path("detail/<int:pk>/", DetailBlogApiView.as_view(), name="detail"),
    #
    # path("update_image/<int:pk>/", UpdateImageApiView.as_view(), name="update_image"),
    #
    # # path("delete/<int:pk>/", BlogDeleteApiview.as_view(), name="delete"),
    #
    # path("image_delete/<int:pk>/", ImageDeleteApiView.as_view(), name="delete_image"),

]
