from django.shortcuts import redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from productstemplate.models import WishList, Order, Product

import datetime
import stripe
import json

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSession(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        url = reverse('home')
        return HttpResponseRedirect(url)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user)
        products = WishList.objects.filter(user=user).order_by('-datatime') # user cart list product
        msg = ""
        check = False
        for product in products:
            stockQuantity = product.product.quantity
            if product.quantity > stockQuantity and stockQuantity != 0:
                msg += f"We don't have enough quantity of {product.product.product_name} in Stock. Product quantity available in stock {stockQuantity}. ||| "
                check = True
                
            elif int(stockQuantity) == 0:
                msg += f"{product.product.product_name} is not available in stock. ||| "
                check = True

        if check == True:
            messages.error(request, msg)
            url = reverse('add-to-cart')
            return HttpResponseRedirect(url)


        line_items = []
        metadata = {}
        for product in products:
            line_items.append(
                {
                    'price_data': {
                        'currency':'BDT',
                        'product_data':{
                            'name': product.product,
                           # 'images':[product.product.image1,]
                        },
                        'unit_amount_decimal': ((product.total_price/product.quantity)*100.0),
                    },
                    'quantity': product.quantity
                }
            )
            metadata['wish_product_id_'+ str(product.id)] = str(product.id)
            metadata['product_id_'+ str(product.product.id)] = str(product.product.id,)
            metadata['specification_'+ str(product.product.id)] = product.product.specification

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
            line_items = line_items,
            phone_number_collection={
                'enabled': True,
            },
            metadata=metadata,
            mode = 'payment',
            success_url = MY_DOMAIN + '/success/',
            cancel_url = MY_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url, code=303)



class SuccessView(View):

    def get(self, request, *args, **kwargs):
        url = reverse('home')
        messages.success(request, 'Payment Successfull.')
        return HttpResponseRedirect(url)


class CancleView(TemplateView):
    template_name = 'payment/cancle.html'



endpoint_secret = settings.WEB_HOOK_SECRETE_KEY

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
        json.loads(payload), endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.create(
        amount=1099*100,
        currency='BDT',
        payment_method_types=['card'],
        receipt_email='abc@gmail.com',
        )
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        # print(payment_intent)

        

    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # print(session)
        # print('\n\n\n')

        shipping = session['customer_details']
        address = shipping['address']
        shping_address = f"{address['country']}, {address['city']}, {address['line1']}, {address['line2']}, Postal Code: {address['postal_code']}"

        # customer_details
        name = shipping['name']
        email = shipping['email']
        phone = shipping['phone']
        # print(name, email, phone)




        # metadata = session['metadata']  # wishList product id

        # price
        subt = session['amount_subtotal']/100
        total_price = session['amount_total']/100
        shiping_cost = total_price - subt


        
        user = User.objects.get(email=email)
        wishlist = WishList.objects.filter(user=user)
        date = datetime.datetime.now()


        summary = ''
        for product in wishlist:
            originalProduct = product.product  # main product
            #decreese the main product quantity 
            originalProduct.quantity = originalProduct.quantity - product.quantity
            if originalProduct.quantity == 0:
                originalProduct.inStock = False  # stack status change
            originalProduct.save() # update the main product quantity
            summary += f"{product.product}  x  {product.quantity}                    Tk {product.total_price}\n"
            userOrder = Order.objects.create(user=user, product=originalProduct,
            quantity=product.quantity, sub_total_price=product.total_price, total_price=total_price,
            shipping_address=shping_address, phone=phone)
        summary += "---------------------------------------------------------\n"
        summary += f"Subtotal                                          {subt}\n"
        summary += f"Shipping                                          {shiping_cost}\n"
        summary += f"Amount charged                                    {total_price}\n"
        summary += "---------------------------------------------------------\n"
        summary += f"Email: {email}, Phone: {phone},\nOrder Time {date}\n"


        userOrder.is_last = True
        userOrder.save()
        wishlist.delete()
        fullmsg = f'Payment Successfull.\nShping Address {shping_address}\n{summary}\n'
        send_mail('Your Online Gadget Store receipt', fullmsg, settings.EMAIL_HOST_USER, [email])
        # Passed signature verification
    return HttpResponse(status=200)








# MM/YY  CVC      02/50  455
# Payment succeeds                   4242 4242 4242 4242
# Payment is declined                4000 0000 0000 9995
# Payment requires authentication    4000 0025 0000 3155
