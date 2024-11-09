import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages

from products.models.carts import Cart, CartProduct
from products.models.customers import Prefecture
from products.models.products import Product
from products.models.promotion_codes import PromotionCode

class CartListView(ListView):
    model = Product
    template_name = "cart/cart.html"

    def get(self, request, *args, **kwargs):
        session_id = request.session.get('session_id')
        if session_id is None:
            return redirect('/')

        self.cart = get_object_or_404(Cart, id=uuid.UUID(session_id))
        cart_products = self.cart.cart_products.all()
        if not cart_products.exists():
            return redirect('/')

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return CartListView.create_context(self.cart, context)
    
    @staticmethod
    def create_context(cart, context={}):
        queryset = cart.calculate_total()
        promotion_code = cart.promotion_code
        context["total"] = cart.total
        context['prefectures'] = Prefecture.objects.all()
        context["carts"] = queryset
        if promotion_code and not promotion_code.is_used:
            context['promotion_code'] = promotion_code
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
        
        product = get_object_or_404(Product, id=uuid.UUID(product_id))
        cart_product, _ = CartProduct.objects.get_or_create(cart=cart, product=product)
        cart_product.quantity += quantity
        cart_product.save()
        return redirect('/cart/')

class DeleteCartView(View):
    def get(self, request, pk):
        session_id = request.session.get('session_id')
        if session_id is None:
            messages.error(request, 'カートが見つかりません。再度お試しください。')
            return redirect('/')
        
        cart = get_object_or_404(Cart, id=uuid.UUID(session_id))
        cart_product = CartProduct.objects.filter(cart=cart, product_id=uuid.UUID(pk)).first()
        if cart_product:
            cart_product.delete()

        return redirect('/cart/')

class ApplyPromotionCode(View):
    def post(self, request):
        session_id = request.session.get('session_id')
        if session_id is None:
            return redirect('/')

        cart = get_object_or_404(Cart, id=session_id)
        promotion_code = request.POST.get('promotion_code')
        if not promotion_code:
            messages.error(self.request, 'プロモーションコードを入力してください。')
            return self._render_context(request, cart)
        codes = PromotionCode.objects.filter(code=promotion_code, is_used=False)
        if not codes.exists():
            messages.error(self.request, '無効なプロモーションコードです。')
            return self._render_context(request, cart)
        promotion_obj = codes.first()
        cart.promotion_code = promotion_obj
        cart.save()
        messages.success(self.request, 'プロモーションコードを適用しました。')
        return self._render_context(request, cart)

    def _render_context(self, request, cart: Cart):
        return render(request, 'cart/cart.html', CartListView.create_context(cart))
        