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

        # Create an order for each product
        for pid in product_ids:
            product = Product.objects.get(id=pid)
            Order.objects.create(
                product=product,
                user_id=None,  # no auth
                total_price=product.price,
                stripe_payment_intent=payment_intent_id,
                status='paid'
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
