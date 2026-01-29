from django.db import models
from products.models import Product
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Order(models.Model):
    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

from django.utils import timezone
from datetime import timedelta


class QRCode(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="qrcodes"
    )
    outlet_name = models.CharField(max_length=100)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.expires_at is None:
            base_time = self.created_at or timezone.now()
            self.expires_at = base_time + timedelta(hours=24)
        super().save(*args, **kwargs)
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.outlet_name} - {self.token}"

