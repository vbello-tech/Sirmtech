from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, View, ListView, DetailView
from .models import Item, Coupon, Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from decimal import Decimal
from common import common
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponse
from phonenumber_field.phonenumber import to_python
from decouple import config


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


def get_grade_price(item, grade):
    if grade == 'A':
        return "Grade A", item.A_price
    elif grade == 'B':
        return "Grade B", item.B_price
    elif grade == 'C':
        return "Grade C", item.C_price
    else:
        raise ValueError("Invalid grade selected")


# function to add to cart
# @login_required(login_url='user:login')
@csrf_protect
@require_http_methods(["POST"])
def place_order(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Get form data
    phone = request.POST.get('phone')
    color = request.POST.get('color')
    size = request.POST.get('size')
    length = request.POST.get('length')
    grade = request.POST.get('grade')
    pieces = int(request.POST.get('pieces', 1))
    add_marker = request.POST.get('addMarker') == 'on'
    fulfillment = request.POST.get('fulfillment')
    address = request.POST.get('address', '')
    text_option = request.POST.get('textOption')
    custom_text = request.POST.get('customTextInput', '')

    phone_number = to_python(phone)

    # Query to check if there's an active order item
    order_item_qs = OrderItem.objects.select_related('item', 'user').filter(
        item=item,
        # user=request.user,
        phone=phone_number,
        ordered=False,
    )
    order_qs = Order.objects.filter(
        # user=request.user,
        ordered=False,
    )
    if order_item_qs.exists():
        messages.success(request, 'You have an active order for this product')
        return redirect('store:product', pk=item.pk)
    else:
        # create order for item.
        grade_label, price = get_grade_price(item, grade)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            # user=request.user,
            phone=phone_number,
            ordered=False,
            colour=color,
            size=size,
            length=length,
            price=price,
            grade=grade_label,
            quantity=pieces,
            marker=add_marker,
            custom_text=custom_text if text_option == "custom" else None
        )
    if order_qs:
        order_qs.items.add(order_item)
        order_qs.address = address
        order_qs.save()
        messages.success(request, 'Your order has been placed. Proceed to cart to complete order!')
        return redirect('store:product', pk=item.pk)
    else:
        order_qs = Order.objects.create(
            # user=request.user,
            phone=phone_number,
            ordered=False, address=address
        ) if fulfillment == "delivery" else Order.objects.create(
            # user=request.user,
            phone=phone_number,
            ordered=False)
        order_qs.items.add(order_item)
        messages.success(request, 'Your order has been placed. Proceed to cart to complete order!')
        return redirect('store:product', pk=item.pk)


# @login_required(login_url='user:login')
def update_cart_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Prefetch user's cart and its related items
    order = (
        Order.objects
        .filter(  # user=request.user,
            ordered=False)
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
    else:
        order.Items.remove(order_item)
        order_item.delete()
        messages.success(request, "Item removed as quantity reached zero.")

    return redirect('store:product', pk=item.pk)


@csrf_exempt
def cart_by_phone(request):
    phone = request.GET.get("phone")
    phone_number = to_python(phone)
    try:
        order = Order.objects.get(phone=phone_number, ordered=False)
        print(order)
        context = {
            "cart_item": order,
            "paystack_public_key": "pk_test_feba4156df35513a5957f20e0ad24bdb65d19284",
            "ref": common.ref(),
        }
    except ObjectDoesNotExist:
        context = {
            "paystack_public_key": "pk_test_feba4156df35513a5957f20e0ad24bdb65d19284",
            "ref": common.ref(),
        }
    html = render_to_string("store/cart_phone.html", context, request=request)
    return HttpResponse(html)


# Place order page
class CompleteOrderView(View):  # LoginRequiredMixin,
    def get(self, request, pk, *args, **kwargs):
        item = get_object_or_404(Item, pk=pk)
        return render(self.request, 'store/complete_order.html', {'item': item})


# VIEW TO DISPLAY ALL AVAILABLE ORDER ITEM THAT THE ORDERED STATUS IS FALSE
class CartView(View):  # LoginRequiredMixin,
    def get(self, *args, **kwargs):
        return render(self.request, 'store/cart.html')


class PaymentVerifyView(View):
    def get(self, request, pk, *args, **kwargs):
        ref = request.GET.get("ref")
        paystack = common.Paystack()
        order = Order.objects.get(pk=pk)

        status, result = paystack.verify_payment(ref, order.total_price())
        if status:
            if result["amount"] / 100 == order.total_price():
                try:
                    order.ordered = True
                    order.payment_id = ref
                    order.ordered_date = timezone.now()
                    order.save()
                    # subject = "NYSC Registration Confirmation"
                    # html_message = render_to_string('nysc/order.html', {'order': order})
                    # plain_message = strip_tags(html_message)
                    # send_mail(subject, plain_message, 'vbellotech@gmail.com', [order.email],
                    #           html_message=html_message)
                    messages.success(self.request, "Your booking was successful. We will send an email to the email "
                                                   "address provided.")
                    return redirect("/")
                except ObjectDoesNotExist:
                    messages.success(self.request, "Your order was not successful")
                    return redirect("/")
        else:
            messages.error(request, 'Your payment could not be verified')
