from django.urls import path
from . import views


# Cart pages
urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='cart_remove'),
    path('increase/<int:product_id>/', views.cart_increase, name='cart_increase'),
    path('decrease/<int:product_id>/', views.cart_decrease, name='cart_decrease'),
    path('checkout/', views.checkout, name='checkout'),
]
