from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product
from .models import Order, OrderItem
from collections import defaultdict
from .models import QRCode
from .utils import create_qr_image
import base64
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required, user_passes_test


def role_select(request):
    return render(request, "registration/role_select.html")


def seller_required(user):
    return user.userprofile.is_seller

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('home')


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

    # 1. Create order
    order = Order.objects.create(
    user=request.user,
    status="PAID"
)


    # 2. Create order items
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty
        )

    # 3. CLEAR cart
    request.session['cart'] = {}

    # 🔥 PHASE 5 STARTS HERE 🔥

    outlet_map = defaultdict(list)
    for item in order.orderitem_set.all():
        outlet_map[item.product.outlet].append(item)

    qr_data = []

    for outlet in outlet_map.keys():
        qr = QRCode.objects.create(
            order=order,
            outlet_name=outlet
        )

        image_bytes = create_qr_image(qr.token)
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        qr_data.append({
            "outlet": outlet,
            "image": image_base64
        })

    # 4. Show QR to student
    return render(request, 'orders/success.html', {
        'order': order,
        'qr_data': qr_data
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})    
    if str(product_id) in cart:
        current_qty=cart[str(product_id)]
        if current_qty > 1:
            cart[str(product_id)] = current_qty-1
        else:
            del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')


def clear_cart(request):
    request.session['cart'] = {}
    return redirect('home')

def generate_qr_codes(order):
    outlet_map = defaultdict(list)

    for item in order.items.all():
        outlet_map[item.product.outlet_name].append(item)

    qrcodes = []
    for outlet in outlet_map.keys():
        qr = QRCode.objects.create(
            order=order,
            outlet_name=outlet
        )
        qrcodes.append(qr)

    return qrcodes



def scan_qr(request):
    if request.method == "POST":
        token = request.POST.get("token")

        try:
            qr = QRCode.objects.get(token=token)
        except QRCode.DoesNotExist:
            return render(request, "orders/scan_qr.html", {
                "error": "Invalid QR code"
            })

        if qr.is_used:
            return render(request, "orders/scan_qr.html", {
                "error": "QR already used"
            })

        qr.is_used = True
        qr.save()

        order = qr.order
        items = order.orderitem_set.filter(
            product__outlet=qr.outlet_name
        )

        return render(request, "orders/claim_items.html", {
            "order": order,
            "items": items,
            "outlet": qr.outlet_name
        })

    return render(request, "orders/scan_qr.html")

@login_required
def student_home(request):
    return render(request, "products/home.html")


def seller_required(user):
    return hasattr(user, "userprofile") and user.userprofile.is_seller


@user_passes_test(seller_required, login_url="/redirect/")
def seller_dashboard(request):

    outlet = request.GET.get("outlet", "MART")
    products = Product.objects.filter(outlet=outlet)

    return render(request, "orders/seller_dashboard.html", {
        "products": products,
        "outlet": outlet
    })


@user_passes_test(seller_required, login_url="/redirect/")
def toggle_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_available = not product.is_available
    product.save()
    return redirect("seller_dashboard")

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/history.html", {"orders": orders})


from django.contrib.auth.decorators import login_required
from .models import Order, QRCode
import base64
from .utils import create_qr_image

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    qr_map = []

    for order in orders:
        qrs = QRCode.objects.filter(order=order)
        qr_data = []

        for qr in qrs:
            image_bytes = create_qr_image(qr.token)
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            qr_data.append({
                "outlet": qr.outlet_name,
                "is_used": qr.is_used,
                "image": image_base64,
            })

        qr_map.append({
            "order": order,
            "qrs": qr_data
        })

    return render(request, "orders/my_orders.html", {
        "qr_map": qr_map
    })
