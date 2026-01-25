from django.urls import path
from .views import home, seller_dashboard, toggle_product

urlpatterns = [
    path('', home, name='home'),
    path('seller/', seller_dashboard, name='seller_dashboard'),
    path('seller/toggle/<int:product_id>/', toggle_product, name='toggle_product'),
]
