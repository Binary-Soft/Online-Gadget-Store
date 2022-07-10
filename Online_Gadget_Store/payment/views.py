from django.shortcuts import redirect, HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from productstemplate.models import WishList, Order, Product

import stripe

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSession(View):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user)
        products = WishList.objects.filter(user=user).order_by('-datatime')[0]

        MY_DOMAIN = 'http://127.0.0.1:8000/user/payments'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=user.email,
           # submit_type='pay',
            shipping_address_collection={
                'allowed_countries': ['BD',],
            },
            shipping_options=[
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {
                            'amount': 50*100,
                            'currency': 'BDT',
                        },
                        'display_name': 'Free shipping',

                        # Delivers between 5-7 business days
                        'delivery_estimate': {
                            'minimum': {
                                'unit': 'business_day',
                                'value': 5,
                            },
                            'maximum': {
                                'unit': 'business_day',
                                'value': 7,
                            },
                        }
                    }
                },
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {
                            'amount': 1000*100,
                            'currency': 'BDT',
                        },
                        'display_name': 'Next day air',
                        # Delivers in exactly 1 business day
                        'delivery_estimate': {
                            'minimum': {
                                'unit': 'business_day',
                                'value': 1,
                            },
                            'maximum': {
                                'unit': 'business_day',
                                'value': 1,
                            },
                        }
                    }
                },
            ],
            line_items = [
                {
                    'price_data': {
                        'currency':'BDT',
                        'product_data':{
                            'name': products.product,
                           # 'images':[products.product.image1,]
                        },
                        'unit_amount_decimal': ((products.total_price/products.quantity)*100.0),
                    },
                    'quantity': products.quantity
                }
            ],
            phone_number_collection={
                'enabled': True,
            },
            metadata={
                'wish_product_id': products.id,
                'product_id':products.product.id,
                'specification':products.product.specification
            },
            mode = 'payment',
            success_url = MY_DOMAIN + '/success/',
            cancel_url = MY_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url, code=303)



class SuccessView(TemplateView):
    template_name = 'payment/success.html'


class CancleView(TemplateView):
    template_name = 'payment/cancle.html'


import json

@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  event = None

  try:
    event = stripe.Event.construct_from(
      json.loads(payload), stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)

  # Handle the event
  if event.type == 'payment_intent.succeeded':
    payment_intent = event.data.object # contains a stripe.PaymentIntent
    print('PaymentIntent was successful!')
  elif event.type == 'payment_method.attached':
    payment_method = event.data.object # contains a stripe.PaymentMethod
    print('PaymentMethod was attached to a Customer!')
  # ... handle other event types
  else:
    print('Unhandled event type {}'.format(event.type))

  return HttpResponse(status=200)








# MM/YY  CVC      02/50  455
# Payment succeeds                   4242 4242 4242 4242
# Payment is declined                4000 0000 0000 9995
# Payment requires authentication    4000 0025 0000 3155
