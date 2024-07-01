from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='mainStore'),
    path('category/<slug:category_slug>/', views.main, name='category'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.productDetails, name='productDetails'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>', views.submit_review, name='submit_review'),
]
