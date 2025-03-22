"""
URL configuration for sirmtech project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("nysc.urls", namespace="nysc")),
]
