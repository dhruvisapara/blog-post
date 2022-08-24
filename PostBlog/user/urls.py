from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordChangeView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from user.views import ProfileView, Upadate, SetNewPassword, UserDeleteView, AddUserView, ShowUser, \
    UserDelete, UpadateStaff, GroupView, UpdatePermission, DeletePermission, GroupList, UserRegistration

app_name = "user"
urlpatterns = [

            # path('', SignUpView.as_view(), name='signup'),
            path('', UserRegistration.as_view(), name='signup'),

            path('login/', LoginView.as_view(), name='login'),
            # path('login/', LoginAPIView.as_view(), name='login'),

            path('logout/', LogoutView.as_view(), name='logout'),
            path('profile/', ProfileView.as_view(), name="profile"),
            path('update/<int:pk>/', Upadate.as_view(), name="update"),
            path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
            path('password-reset-done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
            path('password-reset-confirm/<uidb64>/<token>/', SetNewPassword.as_view(),
                 name='password_reset_confirm'),
            path('change-password', PasswordChangeView.as_view(), name="change-password"),
            path("delete/", UserDeleteView.as_view(), name="delete"),
            path("add_user/",AddUserView.as_view(),name="add_user"),
            path("show_user/",ShowUser.as_view(),name="show_user"),
            path("delete_user/<int:pk>/",UserDelete.as_view(),name="delete_user"),
            path("update_staff/<int:pk>/",UpadateStaff.as_view(),name="update_staff"),
            path("permission/",GroupView.as_view(),name="parmission"),
            path("groupl/",GroupList.as_view(),name="group"),
            path("update_permission/<int:pk>/",UpdatePermission.as_view(),name="update_permission"),
            path("delete_permission/<int:pk>/",DeletePermission.as_view(),name="delete_permission"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
