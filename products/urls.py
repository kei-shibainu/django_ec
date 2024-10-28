from django.urls import path

from products.views.admin_view import AdminProductsView
from products.views.products_view import IndexListView, ProductDetailView

urlpatterns = [
    path("", IndexListView.as_view(), name="products"),
    path("product/<str:pk>", ProductDetailView.as_view(), name="product"),
    path('admin/products/', AdminProductsView.as_view(), name='admin-products'),
]
