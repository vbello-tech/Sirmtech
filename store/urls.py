"""
URL configuration for nysc app.
"""

from django.urls import path
from .views import StoreListView

app_name = "store"

urlpatterns = [
    path('', StoreListView.as_view(), name="list"),
]
