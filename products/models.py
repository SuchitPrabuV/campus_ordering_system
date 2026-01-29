from django.db import models

class Product(models.Model):
    OUTLET_CHOICES = [
        ('CAFE', 'REC Cafe'),
        ('MART', 'REC Mart'),
        ('HUT', 'Hut Cafe'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    outlet = models.CharField(max_length=20, choices=OUTLET_CHOICES)
    location = models.CharField(max_length=100)  # eg: "1st Floor"
    is_available = models.BooleanField(default=True)

    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.outlet}"