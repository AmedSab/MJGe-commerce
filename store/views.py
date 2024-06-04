from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

def main(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        productsCount = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        productsCount = products.count()
    context = {
        'products': products,
        'productsCount': productsCount,
    }
    return render(request, 'store/store.html', context)


def productDetails(request, category_slug=None, product_slug=None):
    try:
        singleProduct = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context= {
        'singleProduct': singleProduct,
    }


    return render(request, 'store/product_details.html', context)
