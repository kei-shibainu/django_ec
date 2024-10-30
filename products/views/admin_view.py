from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from products.forms.admin_forms import ProductForm
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
    template_name = "admin/produict_form.html"
    form_class = ProductForm
    success_url = reverse_lazy('admin-products')

class AdminProductEditView(UpdateView):
    model = Product
    template_name = "admin/produict_form.html"
    form_class = ProductForm
    success_url = reverse_lazy('admin-products')

class AdminProductDeleteView(DeleteView):
    model = Product
    template_name = "admin/produict_confirm_delete.html"
    success_url = reverse_lazy('admin-products')
