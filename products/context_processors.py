import uuid
from products.models.carts import Cart, CartProduct

def cart_count(request):
    session_id = request.session.get('session_id', None)
    if session_id:
        try:
            cart = Cart.objects.get(id=uuid.UUID(session_id))
            cart_count = CartProduct.objects.filter(cart=cart).count()
        except(Cart.DoesNotExist, CartProduct.DoesNotExist):
            cart_count = 0
    else:
        cart_count = 0

    return {
        'cart_count': cart_count,
    }