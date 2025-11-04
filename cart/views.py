from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from store.models import Product


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
        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product_id)

        # Read quantity from form, default to 1
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

        if product_id_str in cart:
            cart[product_id_str]['quantity'] += quantity
        else:
            cart[product_id_str] = {'quantity': quantity, 'price': float(product.price)}

        request.session['cart'] = cart

    return redirect('library')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart  # update session
    return redirect('cart')  # redirect to the cart page


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


def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        # If cart is empty, redirect to library
        return redirect('library')

    products = []
    total = Decimal('0.00')

    # Loop through cart items
    for product_id_str, item_data in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))

        # Extract quantity and price from the item data
        quantity = item_data.get('quantity', 0)
        price = Decimal(str(item_data.get('price', product.price)))

        subtotal = price * quantity
        total += subtotal

        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        # Placeholder for Stripe checkout
        # For now, clear the cart and redirect to success
        request.session['cart'] = {}
        return redirect('success')

    return render(
        request,
        'checkout.html',
        {'cart_items': products, 'total': total}
    )