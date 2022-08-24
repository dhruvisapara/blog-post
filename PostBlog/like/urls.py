from django.urls import path

from like.views import  LikeView

app_name = "user_like"
urlpatterns = [

    path('likes/<int:pk>/', LikeView.as_view(), name='like-blog'),

]
