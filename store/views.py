from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from decimal import Decimal
from .models import Product


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


# Library page (list all products)
def library(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'library.html', {'products': products})


# Product detail page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def success(request):
    return render(request, 'success.html')


# View cart page
def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = Decimal('0.00')

    for product_id_str, item_data in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))

        if isinstance(item_data, dict):
            quantity = item_data.get('quantity', 0)
            price = Decimal(str(item_data.get('price', product.price)))
        else:
            quantity = int(item_data)
            price = product.price

        subtotal = price * quantity
        total += subtotal

        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {'cart_items': products, 'total': total})


# Add product to cart
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('library')  # Redirect back to library page or previous page


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart  # update session
    return redirect('cart')  # redirect to the cart page


# Checkout page (basic placeholder)
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('library')

    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })
        total += product.price * quantity

    if request.method == 'POST':
        # Here you would integrate Stripe checkout
        # For now, we just clear the cart and redirect
        request.session['cart'] = {}
        return redirect('success')

    return render(
        request,
        'store/checkout.html',
        {'cart_items': products, 'total': total}
        )


def cart_increase(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    product_id_str = str(product_id)

    if isinstance(cart.get(product_id_str), int):
        cart[product_id_str] = {
            'quantity': cart[product_id_str],
            'price': float(product.price)
        }

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {'quantity': 1, 'price': float(product.price)}

    request.session['cart'] = cart
    return redirect('cart')


def cart_decrease(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    product_id_str = str(product_id)

    if isinstance(cart.get(product_id_str), int):
        cart[product_id_str] = {
            'quantity': cart[product_id_str],
            'price': float(product.price)
        }

    if product_id_str in cart:
        cart[product_id_str]['quantity'] -= 1
        if cart[product_id_str]['quantity'] <= 0:
            del cart[product_id_str]

    request.session['cart'] = cart
    return redirect('cart')
