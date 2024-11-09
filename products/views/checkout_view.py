import uuid
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages

from django.db import transaction

from products.forms.checkout_forms import CheckOut
from products.models.carts import Cart
from products.models.customers import Customer, Prefecture
from products.models.orders import Order, OrderProduct

from products.models.products import Product
from products.send_message import EmailSender

class CheckOutCreateView(CreateView):
    model = Customer
    form_class = CheckOut
    template_name = "cart/cart.html"
    success_url = reverse_lazy('products')

    def dispatch(self, request, *args, **kwargs):
        session_id = self.request.session.get('session_id')
        if not session_id:
            messages.error(request, 'カートが見つかりません。再度お試しください。')
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        session_id = self.request.session.get('session_id')
        cart = get_object_or_404(Cart, id=session_id)
        customer = form.save()
        queryset = cart.calculate_total()
        
        with transaction.atomic():
            for product in queryset:
                if product['stock'] == 0:
                    messages.error(self.request, f'『{product['name']}』は現在在庫切れです。別の商品をご検討いただくか、後ほど再度ご確認ください。')
                    return self._render_error_context(form, cart, queryset)
                elif product['stock'] < product['quantity']:
                    messages.error(self.request, f'『{product['name']}』は現在、在庫数が「{product['stock']}」です。購入数を減らすか、数量を再確認してください。')
                    return self._render_error_context(form, cart, queryset)

            try:
                order = Order.objects.create(
                    order_id=uuid.uuid4(),
                    customer=customer,
                    total=cart.total,
                    promotion_code=cart.promotion_code,
                )
                for cart_product in cart.cart_products.all():
                    OrderProduct.objects.create(
                        order=order,
                        product=cart_product.product,
                        quantity=cart_product.quantity,
                        total=(cart_product.quantity * cart_product.product.discount_price)
                    )
                    cart_product.product.stock -= cart_product.quantity
                    cart_product.product.save()
                
                if order.promotion_code:
                    order.promotion_code.is_used = True
                    order.promotion_code.save()

                self._send_message(order)
                messages.success(self.request, 'ご購入ありがとうございます！')
                del self.request.session['session_id']
                cart.delete()
            except Exception as e:
                messages.error(self.request, 'メール送信に失敗しました。再度お試しください。')

        return super().form_valid(form)
    
    def _create_message(self, order:Order):
        message = f'''ご注文の確認
注文番号：
{order.order_id}

お届け先：
{order.customer.last_name} {order.customer.first_name} 様
{order.customer.zip}
{order.customer.prefecture.name}
{order.customer.address}
{order.customer.address2}
'''
        if order.promotion_code:
            message += f'''
プロモーションコード適用：
コード　：{order.promotion_code.code}
割引価格：-{order.promotion_code.discount}円
'''         
        message += f'''
商品明細：
合計：{order.total}円
'''
        for order_product in order.orderproduct_set.all():
            message += f'''
商品名：{order_product.product.name}
単価　：{order_product.product.discount_price}円
購入数：{order_product.quantity}
合計　：{order_product.total}
'''
        return message

    def _send_message(self, order: Order):
        message = self._create_message(order)
        to_list = [order.customer.email]
        sender = EmailSender(to_list=to_list, message=message)
        sender.send_message()
    
    def form_invalid(self, form):
        session_id = self.request.session.get('session_id')
        cart = get_object_or_404(Cart, id=session_id)
        queryset = cart.calculate_total()
        return self._render_error_context(form, cart, queryset)

    def _render_error_context(self, form, cart, queryset):
        context = self.get_context_data(form=form)
        context['carts'] = queryset
        context['total'] = cart.total

        prefecture = self.request.POST.get('prefecture')
        prefectures = Prefecture.objects.all()
        context['prefectures'] = prefectures
        context['selected_prefecture'] = uuid.UUID(prefecture)
        promotion_code = cart.promotion_code
        if promotion_code and not promotion_code.is_used:
            context['promotion_code'] = promotion_code
        return self.render_to_response(context=context)
