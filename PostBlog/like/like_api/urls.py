from django.urls import path

from like.like_api.views import LikeApiView

urlpatterns = [

    path("likes/<int:pk>/", LikeApiView.as_view(), name="like"),
]