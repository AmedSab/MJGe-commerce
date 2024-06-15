from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('delete_cart/<int:product_id>/<cart_item_id>/', views.delete_cart, name='delete_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
