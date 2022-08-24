from django.urls import path

from contact.views import ContactAjax
app_name="contact"
urlpatterns = [

    path('contact/', ContactAjax.as_view(), name='contact_submit')
]