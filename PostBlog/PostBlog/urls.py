"""PostBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static

from PostBlog import settings
from django.contrib import admin
from django.urls import include, path
from django.urls import re_path as url
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from contact.admin import contact_admin_site

admin.site.site_header = 'Blog-Post admin'
admin.site.site_title = 'Blog-Post admin'
admin.site.index_title = 'Blog administration'
admin.site.site_url = 'http://127.0.0.1:8000/blog/'
urlpatterns = [

    ################ admin path ########################

    path('admin/', admin.site.urls),
    path('contact-admin/', contact_admin_site.urls),

    ################ Social auth path #################
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    ################ restframwork path #################


    # path('api-auth/', include('rest_framework.urls')),
    # path('api-token-auth', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    ################# blog path ########################
    path("blog/", include('blog.urls')),
    path('', include('blog.blog_api.urls')),

    ################## user path ########################

    path("user/", include('user.urls')),
    path("userapi/", include('user.user_api.urls')),

    ################## like path ########################
    path("like/", include('like.urls')),
    path("like_api/", include('like.like_api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    ################## ajaxuser path ########################
    path("", include('ajaxuser.urls')),
    path("", include('post.urls')),
    path('', include('contact.urls')),
    path('book/', include('book.urls')),
    path('inline/', include('inlineformset.urls')),
    path('game/', include('game.urls')),
    path('chat/', include('chat.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
