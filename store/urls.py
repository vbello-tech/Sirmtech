"""
URL configuration for store app.
"""

from django.urls import path
from .views import (
    StoreListView, ProductView, place_order, update_cart_item, CartView, CompleteOrderView, PaymentVerifyView
)

app_name = "store"

urlpatterns = [
    path('', StoreListView.as_view(), name="list"),
    path('<int:pk>/', ProductView.as_view(), name="product"),
    path('add-to-cart/<int:pk>/', place_order, name="add_to_cart"),
    path('complete-order/<int:pk>/', CompleteOrderView.as_view(), name="complete_order"),
    path('update-cart/<int:pk>/<str:action>/', update_cart_item, name='cart_update'),
    path('cart/', CartView.as_view(), name="cart"),
    path('payment/verify/<int:pk>/', PaymentVerifyView.as_view(), name="verify"),
]
