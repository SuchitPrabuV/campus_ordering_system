from django.shortcuts import render
from .models import Product

def home(request):
    cafes = Product.objects.filter(outlet='CAFE', is_available=True)
    huts = Product.objects.filter(outlet='HUT', is_available=True)
    marts = Product.objects.filter(outlet='MART', is_available=True)

    cart = request.session.get('cart', {})

    return render(request, 'products/home.html', {
        'cafes': cafes,
        'huts': huts,
        'marts': marts,
        'cart': cart
    })
