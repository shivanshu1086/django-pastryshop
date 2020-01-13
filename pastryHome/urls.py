from django.urls import path

from . import views
from .views import (Payment, CheckOutView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart)


app_name = 'pastryHome'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove-single-item-from-cart/<slug>', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', Payment.as_view(), name='payment')
]