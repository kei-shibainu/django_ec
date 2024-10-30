from collections import OrderedDict
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic.list import ListView

from products.models.products import Product

class CartListView(ListView):
    model = Product
    template_name = "cart/cart.html"

    def get(self, request, *args, **kwargs):
        cart = request.session.setdefault('cart', {'products': OrderedDict()})
        if not cart.get('products'):
            return redirect('/')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        cart = self.request.session.setdefault('cart', {'products': OrderedDict()})
        self.queryset = []
        self.total = 0
        for id, quantity in cart['products'].items():
            product = Product.objects.get(pk=id)
            product.quantity = quantity
            product.total = int(product.discount_price * quantity)
            self.queryset.append(product)
            self.total += product.total
        self.request.session['cart'] = cart
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.total
        return context

class AddCartView(View):
    def post(self, request):
        id = request.POST.get('id')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.setdefault('cart', {'products' : OrderedDict()})
        if id in cart['products']:
            cart['products'][id] += quantity
        else:
            cart['products'][id] = quantity
        request.session['cart'] = cart
        return redirect('/cart/')

class DeleteCartView(View):
    def get(self, request, pk):
        cart = self.request.session.get('cart', None)
        if cart is not None:
            del cart['products'][pk]
            request.session['cart'] = cart
        return redirect('/cart/')
