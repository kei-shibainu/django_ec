from django.contrib import admin

from products.models.customers import Customer, Prefecture
from products.models.orders import Order, OrderProduct
from products.models.products import Product

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Customer)
admin.site.register(Prefecture)
