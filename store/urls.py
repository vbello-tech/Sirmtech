"""
URL configuration for store app.
"""

from django.urls import path
from .views import StoreListView, ProductView

app_name = "store"

urlpatterns = [
    path('', StoreListView.as_view(), name="list"),
    path('<int:pk>/', ProductView.as_view(), name="product"),
]
