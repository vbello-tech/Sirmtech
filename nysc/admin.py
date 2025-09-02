from django.contrib import admin
from .models import Nysc, Batch

# Register your models here.

# admin.site.register(Nysc)
admin.site.register(Batch)


@admin.register(Nysc)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'slot', 'payment_status', ]
