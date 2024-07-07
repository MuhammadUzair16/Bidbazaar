# coin_purchase/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CoinPackage, Purchase
import json
import stripe
from .stripe_config import stripe

@login_required
def buy_now(request):
    coin_packages = CoinPackage.objects.filter(available=True)
    return render(request, 'coin_purchase/buy_now.html', {'coin_packages': coin_packages})

@csrf_exempt
@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            package_id = data.get('package_id')
            coin_package = CoinPackage.objects.get(id=package_id)

            # Create a Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': coin_package.name,
                        },
                        'unit_amount': int(coin_package.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/coin_purchase/payment_done/'),
                cancel_url=request.build_absolute_uri('/coin_purchase/payment_cancelled/'),
            )

            return JsonResponse({'id': session.id})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format in request.'})

        except CoinPackage.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Coin package does not exist.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
@login_required
def payment_done(request):
    # Mark purchase as successful
    user = request.user
    # Assuming you have the package ID in session or another means to retrieve the recent purchase
    package_id = request.session.get('package_id')
    coin_package = CoinPackage.objects.get(id=package_id)

    # Create purchase record
    Purchase.objects.create(user=user, coin_package=coin_package, successful=True)

    # Clear the session
    del request.session['package_id']

    return render(request, 'coin_purchase/payment_done.html')

@csrf_exempt
@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            package_id = data.get('package_id')
            coin_package = CoinPackage.objects.get(id=package_id)

            # Store package ID in session
            request.session['package_id'] = package_id

            # Create a Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': coin_package.name,
                        },
                        'unit_amount': int(coin_package.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/coin_purchase/payment_done/'),
                cancel_url=request.build_absolute_uri('/coin_purchase/payment_cancelled/'),
            )

            return JsonResponse({'id': session.id})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format in request.'})

        except CoinPackage.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Coin package does not exist.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
def payment_cancelled(request):
    # Handle cancelled payment here
    return render(request, 'coin_purchase/payment_cancelled.html')
