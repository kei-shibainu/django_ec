from django.urls import path

from products.views.admin_view import AdminProductsView, AdminProductCreateView, AdminProductEditView, AdminProductDeleteView
from products.views.cart_views import AddCartView, CartListView, DeleteCartView
from products.views.products_view import IndexListView, ProductDetailView

urlpatterns = [
    path("", IndexListView.as_view(), name="products"),
    path("product/<str:pk>", ProductDetailView.as_view(), name="product"),
    path('admin/products/', AdminProductsView.as_view(), name='admin-products'),
    path('admin/product/create/', AdminProductCreateView.as_view(), name='admin-create-product'),
    path('admin/product/edit/<str:pk>', AdminProductEditView.as_view(), name='admin-update-product'),
    path('admin/product/delete/<str:pk>', AdminProductDeleteView.as_view(), name='admin-delete-product'),
    path("cart/", CartListView.as_view(), name="cart"),
    path("cart/add/", AddCartView.as_view(), name="cart-add"),
    path("cart/delete/<str:pk>/", DeleteCartView.as_view(), name="cart-delete"),
]
