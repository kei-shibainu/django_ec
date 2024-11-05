from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from products.forms.admin_forms import ProductForm
from products.models.carts import CartProduct
from products.models.products import Product
from products.views.basic_auth_view import BasicAuthMixIn

class AdminProductsView(BasicAuthMixIn, ListView):
    model = Product
    template_name = "index.html"
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Book Shop -管理者商品一覧'
        return context

class AdminProductCreateView(BasicAuthMixIn, CreateView):
    model = Product
    template_name = "admin/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy('admin-products')

class AdminProductEditView(BasicAuthMixIn, UpdateView):
    model = Product
    template_name = "admin/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy('admin-products')

class AdminProductDeleteView(BasicAuthMixIn, View):
    template_name = "admin/product_confirm_delete.html"

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'object': product})

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        product.is_deleted = True
        product.save()
        CartProduct.objects.filter(product=product).delete()
        return redirect(reverse_lazy('admin-products'))
