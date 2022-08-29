from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from pizzeria.models import Topping, Pizza


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_soldout')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('not_soldout/', self.set_not_soldout),
            path('soldout/', self.set_soldout),
        ]
        return my_urls + urls

    def set_soldout(self, request):
        self.model.objects.all().update(is_soldout=True)
        self.message_user(request, "Pizzas are soldout.")
        return HttpResponseRedirect("../")

    def set_not_soldout(self, request):
        self.model.objects.all().update(is_soldout=False)
        self.message_user(request, "All pizzas are available")
        return HttpResponseRedirect("../")
