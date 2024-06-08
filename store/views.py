from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.models import CartItem, Cart
from cart.views import _getOrCreateSessionKey
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

def main(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        productsCount = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        productsCount = products.count()
    context = {
        'products': paged_products,
        'productsCount': productsCount,
    }
    return render(request, 'store/store.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            productsCount = products.count()

    context = {
    'products': products,
    'productsCount': productsCount,

    }
    return render(request, 'store/store.html', context)


def productDetails(request, category_slug=None, product_slug=None):
    try:
        singleProduct = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_getOrCreateSessionKey(request), product=singleProduct).exists()
    except Exception as e:
        raise e

    context= {
        'singleProduct': singleProduct,
        'in_cart': in_cart,
    }


    return render(request, 'store/product_details.html', context)
