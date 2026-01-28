from django.contrib import admin
from .models import Order, OrderItem, QRCode

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(QRCode)


# Register your models here.
