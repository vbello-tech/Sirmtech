from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, View, ListView, DetailView
from .models import Item, Coupon, Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages
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


@login_required(login_url='user:login')
def add_to_cart(request, pk):
    # Use select_related if Item has foreign keys (e.g., category, brand)
    item = get_object_or_404(Item, pk=pk)

    # Get or create the OrderItem for this user and item
    order_item, created = OrderItem.objects.select_related('item', 'user').get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    # Fetch or create the active Order for the user, prefetching items to avoid repeated queries
    order, created_order = Order.objects.prefetch_related(
        'items__item'
    ).get_or_create(
        user=request.user,
        ordered=False,
    )

    # Check if the item is already in the order
    if order.items.filter(item__pk=item.pk).exists():
        order_item.quantity += 1
        order_item.save()
        messages.info(request, "This item's quantity was increased.")
    else:
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")

    return redirect('store:product', pk=item.pk)


@login_required(login_url='user:login')
def update_cart_item(request, pk, action):
    item = get_object_or_404(Item, pk=pk)

    # Prefetch user's cart and its related items
    order = (
        Order.objects
        .filter(user=request.user, ordered=False)
        .prefetch_related(
            Prefetch('Items', queryset=OrderItem.objects.select_related('item'))
        )
        .first()
    )

    if not order:
        messages.warning(request, "No active cart found.")
        return redirect('store:product', pk=item.pk)

    # Check if the item exists in the order
    order_item = order.Items.filter(item=item).first()

    if not order_item:
        messages.warning(request, "This item is not in your cart.")
        return redirect('store:product', pk=item.pk)

    if action == "remove":
        order.Items.remove(order_item)
        order_item.delete()
        messages.success(request, "This item was removed from your cart.")
    elif action == "decrease":
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
            messages.success(request, "This item quantity was reduced.")
        else:
            order.Items.remove(order_item)
            order_item.delete()
            messages.success(request, "Item removed as quantity reached zero.")
    else:
        messages.error(request, "Invalid action.")

    return redirect('store:product', pk=item.pk)


# VIEW TO DISPLAY ALL AVAILABLE ORDER ITEM THAT THE ORDERED STATUS IS FALSE
class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order,
            }
            return render(self.request, 'store/cart.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'store/cart.html')

    def post(self, *args, **kwargs):
        pass
