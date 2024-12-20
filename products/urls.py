from django.urls import path

from products.views.admin_view import AdminProductsView, AdminProductCreateView, AdminProductEditView, AdminProductDeleteView
from products.views.cart_views import AddCartView, ApplyPromotionCode, CartListView, DeleteCartView
from products.views.checkout_view import CheckOutCreateView
from products.views.order_history_views import OrderDetailView, OrderListView
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
    path("cart/promotion/", ApplyPromotionCode.as_view(), name="cart-promotion"),
    path("cart/checkout/", CheckOutCreateView.as_view(), name="cart-checkout"),
    path("admin/orders/", OrderListView.as_view(), name="admin-orders"),
    path("admin/orders/<str:pk>", OrderDetailView.as_view(), name="admin-order"),
]
