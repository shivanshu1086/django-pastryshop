from django.contrib import admin
from .models import Pastry, Blogs, OrderItem, Order, Billing
# Register your models here.

admin.site.register(Pastry)
admin.site.register(Blogs)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Billing)