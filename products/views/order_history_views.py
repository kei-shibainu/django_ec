from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from products.models.orders import Order
from products.views.basic_auth_view import BasicAuthMixIn

class OrderListView(BasicAuthMixIn, ListView):
    model = Order
    template_name = "admin/order_list.html"
    context_object_name = 'orders'

class OrderDetailView(BasicAuthMixIn, DetailView):
    model = Order
    template_name = "admin/order.html"
    context_object_name = 'order'

