from django.urls import path

from book.views import create_book_model_form

urlpatterns = [
                  path("", create_book_model_form, name='book')
]
