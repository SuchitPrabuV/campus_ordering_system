from django.urls import path
from .views import add_to_cart, view_cart, place_order, remove_from_cart, clear_cart

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('place/', place_order, name='place_order'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear/', clear_cart, name='clear_cart'),

]
