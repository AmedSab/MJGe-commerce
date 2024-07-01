from django.shortcuts import render, redirect
from .models import Cart, CartItem
from store.models import Product , Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

def _getOrCreateSessionKey(request):
    id = request.session.session_key
    if not id:
        id = request.session.create()
    return id

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    if user.is_authenticated:
        product_variations = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_getOrCreateSessionKey(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_getOrCreateSessionKey(request))
        cart.save()


        is_cartItem = CartItem.objects.filter(product=product, user=user).exists()
        if is_cartItem:
            cartItem = CartItem.objects.filter(product=product, user=user)
            cartItemsVariations = []
            id = []

            for i in cartItem:
                # i.variations.all()
                cartItemsVariations.append(list(i.variations.all()))
                id.append(i.id)

            if product_variations in cartItemsVariations:
                index = cartItemsVariations.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, user=user, quantity=1)
                if len(product_variations) > 0:
                    item.variations.clear()
                    for i in product_variations:
                        item.variations.add(i)
                item.save()

        else:
            cartItem = CartItem.objects.create(product=product, user=user, quantity=1, cart=cart)
            if len(product_variations) > 0:
                cartItem.variations.clear()
                for item in product_variations:
                    cartItem.variations.add(item)
            cartItem.save()
        return redirect('main')
        # //////////////////////////////////////////////////
    else:

        product_variations = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id=_getOrCreateSessionKey(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_getOrCreateSessionKey(request))
        cart.save()


        is_cartItem = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cartItem:
            cartItem = CartItem.objects.filter(product=product, cart=cart)
            cartItemsVariations = []
            id = []

            for i in cartItem:
                # i.variations.all()
                cartItemsVariations.append(list(i.variations.all()))
                id.append(i.id)

            if product_variations in cartItemsVariations:
                index = cartItemsVariations.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, cart=cart, quantity=1)
                if len(product_variations) > 0:
                    item.variations.clear()
                    for i in product_variations:
                        item.variations.add(i)
                item.save()

        else:
            cartItem = CartItem.objects.create(product=product, cart=cart, quantity=1)
            if len(product_variations) > 0:
                cartItem.variations.clear()
                for item in product_variations:
                    cartItem.variations.add(item)
            cartItem.save()
        return redirect('main')


def remove_cart(request, product_id, cart_item_id):

    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cartItem = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_getOrCreateSessionKey(request))
            cartItem = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cartItem.quantity > 1:
            cartItem.quantity -= 1
            cartItem.save()
        else:
            cartItem.delete()
    except:
        pass
    return redirect('main')


def delete_cart(request, product_id, cart_item_id):

    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cartItem = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_getOrCreateSessionKey(request))
            cartItem = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cartItem.delete()
    except:
        pass
    return redirect('main')


def main(request, total=0, quantity=0, cartItems=None):
    try:
        if request.user.is_authenticated:
            cartItems = CartItem.objects.all().filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_getOrCreateSessionKey(request))
            cartItems = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cartItems:
            total += int(item.sub_total())
            quantity += item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
    'total': total,
    'quantity': quantity,
    'cartItems': cartItems,
    }

    return render(request, 'cart/cart.html', context)
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cartItems=None):
    try:
        if request.user.is_authenticated:
            cartItems = CartItem.objects.all().filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_getOrCreateSessionKey(request))
            cartItems = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cartItems:
            total += int(item.sub_total())
            quantity += item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
    'total': total,
    'quantity': quantity,
    'cartItems': cartItems,
    }
    return render(request, 'cart/checkout.html', context)
