from django.shortcuts import render
from .models import Product

def home(request):

    query = request.GET.get("q", "")
    cafes = Product.objects.filter(outlet='CAFE', is_available=True)
    huts = Product.objects.filter(outlet='HUT', is_available=True)
    marts = Product.objects.filter(outlet='MART', is_available=True)
    
    if query:
        cafes = cafes.filter(name__icontains=query)
        huts  = huts.filter(name__icontains=query)
        marts = marts.filter(name__icontains=query)

    cart = request.session.get('cart', {})

    return render(request, 'products/home.html', {
        'cafes': cafes,
        'huts': huts,
        'marts': marts,
        'cart': cart, 
        'query':query
    })
