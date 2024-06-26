from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from cart.models import CartItem, Cart
from cart.views import _getOrCreateSessionKey
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewRatingForm
from django.contrib import messages
from orders.models import OrderProduct

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

    if request.user.is_authenticated:

        try:
            orderProduct = OrderProduct.objects.filter(user=request.user, product__id=singleProduct.id).exists()
        except OrderProduct.DoesNotExist:
            orderProduct = None
    else:
        orderProduct = None

    reviews = ReviewRating.objects.filter(product_id=singleProduct.id, status=True)

    product_gallery = ProductGallery.objects.filter(product_id=singleProduct.id)

    context= {
        'singleProduct': singleProduct,
        'in_cart': in_cart,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }


    return render(request, 'store/product_details.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewRatingForm(request.POST, instance=review)
            form.save()
            messages.success(request, 'Your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Your review has been submitted')
                return redirect(url)

    return render(request, 'store/product_details.html')
