import random
import string
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

LABEL_CHOICES = (
    ('NEW', 'NEW'),
    ('FEATURED', 'FEATURED'),
    ('SPECIAL', 'SPECIAL'),
)

LENGTH_CHOICES = (
    ('SHORT SLEEVE', 'SHORT SLEEVE'),
    ('LONG SLEEVE', 'LONG SLEEVE'),
)

SIZE_CHOICES = (
    ('xs', 'xs'),
    ('xm', 'xm'),
    ('xl', 'xl'),
)


def product_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


class Item(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    image = models.ImageField(blank=False, upload_to="StoreImages/")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, choices=LABEL_CHOICES)
    # category = models.CharField(max_length=100, blank=True, choices=CATEGORY_CHOICES)
    in_stock = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_detail(self):
        return reverse("store:product", kwargs={
            'pk': self.pk,
        })

    def add_to_cart(self):
        return reverse("store:add_to_cart", kwargs={
            'pk': self.pk,
        })

    def remove_from_cart(self):
        return reverse("store:cart_update", kwargs={
            'pk': self.pk,
            'action': "remove",
        })

    def decrease_cart_item(self):
        return reverse("store:cart_update", kwargs={
            'pk': self.pk,
            'action': "decrease",
        })

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    colour = models.CharField(max_length=300, blank=True, null=True)
    length = models.CharField(max_length=100, blank=True, choices=LENGTH_CHOICES, null=True)
    size = models.CharField(max_length=100, blank=True, choices=SIZE_CHOICES, null=True)
    quantity = models.IntegerField(default=1)
    in_cart = models.BooleanField(default=False)

    def get_total_price(self):
        return self.quantity * self.item.price

    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_price()

    def __str__(self):
        return f"{self.quantity} of {self.item.name} "


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    closed = models.BooleanField(default=False, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} order"

    def total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.price
        return total

    # def get_paystack_verify_url(self):
    #     return reverse("collection:paystackverify", kwargs={
    #         'pk': self.pk,
    #     })


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    price = models.IntegerField()

    def __str__(self):
        return self.code
