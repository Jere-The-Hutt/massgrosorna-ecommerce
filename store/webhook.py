import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from .models import Order, Product

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)  # Invalid signature

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_intent_id = session.get('payment_intent')

        # Extract metadata
        product_ids_str = session.get('metadata', {}).get('product_ids', "")
        product_ids = [int(pid) for pid in product_ids_str.split(",") if pid]
        session_key = session.get('metadata', {}).get('session_key')

        # Calculate total_price
        total_price = 0
        for pid in product_ids:
            try:
                product = Product.objects.get(id=pid)
                total_price += product.price
            except Product.DoesNotExist:
                continue

        # Extract shipping info from customer_details
        customer_details = session.get('customer_details', {})

        shipping_name = customer_details.get('name')
        shipping_email = customer_details.get('email')

        addr = customer_details.get('address', {})
        shipping_address = ", ".join(filter(None, [
            addr.get('line1'),
            addr.get('line2'),
            addr.get('city'),
            addr.get('postal_code'),
            addr.get('country'),
        ])) if addr else None

        # Create a single order for all products
        if product_ids:
            Order.objects.create(
                products=",".join([str(pid) for pid in product_ids]),
                total_price=total_price,
                user_id=None,  # no auth
                stripe_payment_intent=payment_intent_id,
                status='paid',
                shipping_name=shipping_name,
                shipping_email=shipping_email,
                shipping_address=shipping_address
            )

        # Clear the cart for this session
        if session_key:
            try:
                sess = Session.objects.get(session_key=session_key)
                data = sess.get_decoded()
                data['cart'] = {}
                sess.session_data = Session.objects.encode(data)
                sess.save()
            except Session.DoesNotExist:
                pass

    return HttpResponse(status=200)
