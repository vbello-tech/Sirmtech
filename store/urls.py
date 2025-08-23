"""
URL configuration for store app.
"""

from django.urls import path
from .views import (
    StoreListView, ProductView, place_order, update_cart_item, CartView, CompleteOrderView, PaymentVerifyView,
    cart_by_phone, admin_orders_view, close_order_view, refresh_orders_view
)

app_name = "store"

urlpatterns = [
    path('', StoreListView.as_view(), name="list"),
    path('<int:pk>/', ProductView.as_view(), name="product"),
    path('add-to-cart/<int:pk>/', place_order, name="add_to_cart"),
    path('complete-order/<int:pk>/', CompleteOrderView.as_view(), name="complete_order"),
    path('update-cart/<int:pk>/<str:action>/', update_cart_item, name='cart_update'),
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/phone/', cart_by_phone, name='phone_cart'),
    path('payment/verify/<int:pk>/', PaymentVerifyView.as_view(), name="verify"),
    path('admin/', admin_orders_view, name='order_admin'),
    path('admin/close-order/<order_id>/', close_order_view, name="close_order"),
    path('admin/refresh-orders/', refresh_orders_view, name="refresh_order"),
]
