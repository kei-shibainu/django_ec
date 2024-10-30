from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from products.models.products import Product

class IndexListView(ListView):
    model = Product
    template_name = "index.html"
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Book Shop - 商品一覧'
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product.html"
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_products"] = Product.objects.order_by('-created_at')[:4]
        return context
    
    