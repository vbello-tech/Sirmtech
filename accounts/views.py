from django.shortcuts import render
from django.views.generic import View


# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registrations/home.html',)


class CatalogueView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registrations/catalogue.html',)

