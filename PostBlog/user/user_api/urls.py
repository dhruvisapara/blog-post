from django.urls import path, include
from rest_framework import routers

from user.user_api.views import *
router=routers.SimpleRouter()
router.register(r'user', UserViewSet, basename="user")
urlpatterns = [
    path('',include(router.urls)),
    path("register/", RegisterAPI.as_view(), name="register"),
    # path("logout/", Logout.as_view(), name="logout"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/api/", UserAPIView.as_view(),name='get-details'),
    path("login/", MyObtainTokenPairView.as_view(),name='api-login'),
    path("change-password/", ChangePasswordView.as_view(),name='change-password'),
]
