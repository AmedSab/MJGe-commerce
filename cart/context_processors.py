from .models import Cart, CartItem
from .views import _getOrCreateSessionKey

def counter(request):
    cartCount = 0
    # if 'admin' in request.path:
    #     return {}
    try:
        cart = Cart.objects.filter(cart_id= _getOrCreateSessionKey(request))
        cartItems = CartItem.objects.all().filter(cart=cart[:1])
        for item in cartItems:
            cartCount += item.quantity
    except Cart.DoesNotExist:
        cartCount = 0
    return dict(cartCount=cartCount)
