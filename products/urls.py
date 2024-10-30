from django.urls import path

from products.views.admin_view import AdminProductsView, AdminProductCreateView, AdminProductEditView, AdminProductDeleteView
from products.views.products_view import IndexListView, ProductDetailView

urlpatterns = [
    path("", IndexListView.as_view(), name="products"),
    path("product/<str:pk>", ProductDetailView.as_view(), name="product"),
    path('admin/products/', AdminProductsView.as_view(), name='admin-products'),
    path('admin/product/create/', AdminProductCreateView.as_view(), name='admin-create-product'),
    path('admin/product/edit/<str:pk>', AdminProductEditView.as_view(), name='admin-update-product'),
    path('admin/product/delete/<str:pk>', AdminProductDeleteView.as_view(), name='admin-delete-product'),
]
