import uuid
from django.db import models

from products.models.customers import Customer
from products.models.products import Product
from products.models.promotion_codes import PromotionCode

class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True, verbose_name='注文日')
    product = models.ManyToManyField(Product, through='OrderProduct')
    total = models.PositiveIntegerField(default=0)
    promotion_code = models.ForeignKey(PromotionCode, on_delete=models.SET_NULL, related_name='order', null=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-order_date']

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'order_products'
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique_order_product')
        ]