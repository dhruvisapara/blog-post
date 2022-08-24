from django.urls import path
from game.views import index, game

urlpatterns = [
    path('', index),
    path('play/<room_code>', game),
]

