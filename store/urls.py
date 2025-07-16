"""
URL configuration for store app.
"""

from django.urls import path
from .views import StoreListView, ProductView, add_to_cart, update_cart_item, CartView

app_name = "store"

urlpatterns = [
    path('', StoreListView.as_view(), name="list"),
    path('<int:pk>/', ProductView.as_view(), name="product"),
    path('add-to-cart/<int:pk>/', add_to_cart, name="add_to_cart"),
    path('update-cart/<int:pk>/<str:action>/', update_cart_item, name='cart_update'),
    path('cart/', CartView.as_view(), name="cart"),
]
