from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product
from .models import Order, OrderItem


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        items.append({
            'product': product,
            'qty': qty,
            'subtotal': product.price * qty
        })
        total += product.price * qty

    return render(request, 'orders/cart.html', {
        'items': items,
        'total': total
    })


def place_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('home')

    order = Order.objects.create(status='PAID')

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty
        )

    request.session['cart'] = {}
    return render(request, 'orders/success.html', {'order': order})
