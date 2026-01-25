from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def home(request):
    cafes = Product.objects.filter(outlet='CAFE', is_available=True)
    huts = Product.objects.filter(outlet='HUT', is_available=True)
    marts = Product.objects.filter(outlet='MART', is_available=True)

    return render(request, 'products/home.html', {
        'cafes': cafes,
        'huts': huts,
        'marts': marts,
    })

def seller_dashboard(request):
    outlet = 'CAFE'  # change later for Hut / Mart
    products = Product.objects.filter(outlet=outlet)

    return render(request, 'products/seller_dashboard.html', {
        'products': products,
        'outlet': outlet
    })

def toggle_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_available = not product.is_available
    product.save()
    return redirect('seller_dashboard')
