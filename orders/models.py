from django.db import models
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
    ]

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


# Create your models here.
