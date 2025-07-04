from django.shortcuts import render
from django.views.generic import CreateView, View, ListView, DetailView
from .models import Item, Coupon
# Create your views here.


class StoreListView(ListView):
    """
    View for all blog list
    """
    model = Item
    context_object_name = "items"
    template_name = "store/list.html"

    # Queryset to render all blog from db in order of publish_date (newest first)
    def get_queryset(self):
        return Item.objects.order_by('-created_date')


class ProductView(DetailView):
    """
    View for all blog list
    """
    model = Item
    context_object_name = "item"
    template_name = "store/product.html"

