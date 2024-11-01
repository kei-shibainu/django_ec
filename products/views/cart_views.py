import uuid
from django.shortcuts import redirect
from django.views import View
from django.views.generic.list import ListView

from products.models.carts import Cart, CartProduct
from products.models.products import Product

class CartListView(ListView):
    model = Product
    template_name = "cart/cart.html"

    def get(self, request, *args, **kwargs):
        session_id = request.session.get('session_id', None)
        if session_id is None:
            return redirect('/')

        try:
            self.cart = Cart.objects.get(id=uuid.UUID(session_id))
            self.cart_products = self.cart.cart_products.all()
            if not self.cart_products.exists():
                return redirect('/')
        except (Cart.DoesNotExist):
            return redirect('/')

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.cart.calculate_total()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.cart.total
        return context

class AddCartView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        session_id = request.session.get('session_id')

        if session_id:
            cart, _ = Cart.objects.get_or_create(id=uuid.UUID(session_id))
        else:
            cart = Cart.objects.create()
            request.session['session_id'] = str(cart.id)
        
        product = Product.objects.filter(id=uuid.UUID(product_id)).first()
        if product:
            cart_product, _ = CartProduct.objects.get_or_create(cart=cart, product=product)
            cart_product.quantity += quantity
            cart_product.save()
        return redirect('/cart/')

class DeleteCartView(View):
    def get(self, request, pk):
        session_id = request.session.get('session_id')
        if not session_id:
            return redirect('/') 

        try:
            cart = Cart.objects.get(id=uuid.UUID(session_id))
            cart_product = CartProduct.objects.get(cart=cart, product_id=uuid.UUID(pk))
            cart_product.delete()
        except(Cart.DoesNotExist, CartProduct.DoesNotExist):
            pass
        return redirect('/cart/')
