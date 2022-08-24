from django.urls import path

from post.views import create_post,  create_post_view, blog_view

urlpatterns=[
path("create/", create_post, name='home'),

    path('option/', blog_view, name='blog'),
    path('create-post/', create_post_view, name='create-post')
]