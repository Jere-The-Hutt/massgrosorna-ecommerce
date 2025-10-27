from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('library/', views.library, name='library'),
    path('success/', views.success, name='success'),

    # Product detail page
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
        ),

    # Cart pages
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    ]
