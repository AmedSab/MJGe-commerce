from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<slug:category_slug>/', views.main, name='category'),
    path('<slug:category_slug>/<slug:product_slug>', views.productDetails, name='productDetails'),
]
