from django.views.generic.list import ListView

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
