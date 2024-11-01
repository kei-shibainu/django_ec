import uuid
from django.db import models
from products.models.products import Product

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'carts'

    def calculate_total(self):
        queryset = []
        self.total = 0

        for cart_product in self.cart_products.all():
            product = cart_product.product
            product_info = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'quantity': cart_product.quantity,
                'sub_total': int(product.discount_price * cart_product.quantity),
            }
            queryset.append(product_info)
            self.total += product_info['sub_total']
        return queryset

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.PositiveIntegerField(default=0, verbose_name='数量')

    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        db_table = 'cart_products'
        unique_together = ('cart', 'product')

