from django.shortcuts import render
from django.views.generic import View


# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registrations/home.html',)


class CatalogueView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registrations/catalogue.html',)


# handle 404 error
def handler404(request, exception):
    context = {"<h1>PAGE NOT FOUND!! ARE YOU SURE YOU ARE NAVIGATING TO THE RIGHT PAGE?</h1>"}
    response = render(request, "templates/404.html", context)
    response.status_code = 404
    return response


# handle 500 error
def handler500(request):
    context = {"<h1>OOPS !!! <br> SEVER ERROR!!! <br> </h1>"}
    response = render(request, "templates/500.html", context)
    response.status_code = 500
    return response
