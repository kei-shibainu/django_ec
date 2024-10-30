from collections import OrderedDict
from products.models.products import Product

def cart_count(request):
    cart = request.session.setdefault('cart', {'products': OrderedDict()})

    # 存在しないカート情報の場合はカートから商品を削除(カート追加後に商品が削除された場合の考慮)
    removes = []
    for id in list(cart.get('products').keys()):
        try:
            Product.objects.get(pk=id)
        except Product.DoesNotExist:
            del cart['products'][id]
    request.session['cart'] = cart

    return {
        'cart_count': len(cart.get('products', OrderedDict()).values()),
        'cart': cart,
    }