from django.urls import path, include
from . import views
from .webhook import stripe_webhook


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('library/', views.library, name='library'),
    path('success/', views.success, name='success'),
    path('footer-contact/', views.footer_contact, name='footer_contact'),


    # Product detail page
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
        ),

    path('cart/', include('cart.urls')),  # this handles the /cart/ prefix
    path('stripe/webhook/', stripe_webhook, name='stripe_webhook'),
    ]
