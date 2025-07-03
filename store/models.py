import random
import string
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.conf import settings

# Create your models here.

LABEL_CHOICES = (
    ('NEW', 'NEW'),
    ('FEATURED', 'FEATURED'),
    ('SPECIAL', 'SPECIAL'),
)


def product_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


class Item(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=False)
    colour = models.CharField(max_length=300, blank=False)
    image = models.ImageField(blank=False, upload_to="StoreImages/")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, choices=LABEL_CHOICES)
    # category = models.CharField(max_length=100, blank=True, choices=CATEGORY_CHOICES)
    pieces = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def get_detail(self):
        return reverse("collection:detail", kwargs={
            'pk': self.pk,
            'code': self.product_code,
            'name': self.name
        })

    def __str__(self):
        return self.name


#
# class OrderItem(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     in_cart = models.BooleanField(default=False)
#
#     def get_total_price(self):
#         return self.quantity * self.collection.price
#
#     def get_total_discount_price(self):
#         return self.quantity * self.collection.discount_price
#
#     def get_final_price(self):
#         if self.collection.discount_price:
#             return self.get_total_discount_price()
#         return self.get_total_price()
#
#     def __str__(self):
#         return f"{self.quantity} of {self.collection.name} "
#
#
# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ref_code = models.CharField(max_length=20, blank=True, null=True)
#     collections = models.ManyToManyField(OrderItem)
#     ordered_date = models.DateTimeField(auto_now_add=True)
#     ordered = models.BooleanField(default=False)
#     closed = models.BooleanField(default=False, blank=True, null=True)
#     address = models.CharField(max_length=1000, blank=True, null=True)
#     phone = models.BigIntegerField(blank=True, null=True, help_text='Contact phone number',
#                                    validators=[RegexValidator(r'^\d{4}-\d{3}-\d{4}$')])
#     coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.user.username} order"
#
#     def total_price(self):
#         total = 0
#         for order_item in self.collections.all():
#             total += order_item.get_final_price()
#         if self.coupon:
#             total -= self.coupon.price
#         return total
#
#     def get_paystack_verify_url(self):
#         return reverse("collection:paystackverify", kwargs={
#             'pk': self.pk,
#         })


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    price = models.IntegerField()

    def __str__(self):
        return self.code
