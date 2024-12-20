import uuid
from products.models.carts import Cart, CartProduct

def cart_count(request):
    session_id = request.session.get('session_id', None)
    if session_id:
        try:
            cart = Cart.objects.get(id=uuid.UUID(session_id))
            cart_count = cart.cart_products.filter(product__is_deleted=False).count()
        except(Cart.DoesNotExist):
            cart_count = 0
    else:
        cart_count = 0

    return {
        'cart_count': cart_count,
    }