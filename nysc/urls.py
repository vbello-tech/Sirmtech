"""
URL configuration for nysc app.
"""

from django.urls import path
from .views import NyscView, PaymentView, PaymentVerifyView, GeneratePdf, SlotPreviewView, edit_booking

app_name = "nysc"

urlpatterns = [
    path('', NyscView.as_view(), name="form"),
    path('payment/<int:pk>/', PaymentView.as_view(), name="payment"),
    path('payment/verify/<int:pk>/', PaymentVerifyView.as_view(), name="verify"),
    path('slot/preview/<int:pk>/', SlotPreviewView.as_view(), name="preview"),
    path('slot/edit/<int:pk>/', edit_booking, name="edit"),
    path('slot/generate-pdf/<int:pk>/', GeneratePdf.as_view(), name="generate_pdf"),
]
