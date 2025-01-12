from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CoinPackage, Purchase
from accounts.models import Account, Profile
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


            request.session['package_id'] = package_id


            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': coin_package.name,
                        },
                        'unit_amount': int(coin_package.coin_price * 100),
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
def payment_done(request):
    user = request.user
    package_id = request.session.get('package_id')

    if package_id:
        try:
            coin_package = CoinPackage.objects.get(id=package_id)
            purchase = Purchase.objects.create(user=user, coin_package=coin_package, successful=True)


            try:
                profile = user.profile
                profile.coins += coin_package.coins
                profile.save()
            except Profile.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User profile does not exist.'})

            del request.session['package_id']

            return render(request, 'coin_purchase/payment_done.html', {'purchase': purchase})

        except CoinPackage.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Coin package does not exist.'})
    else:
        return JsonResponse({'success': False, 'message': 'No package ID found in session.'})

@login_required
def payment_cancelled(request):

    return render(request, 'coin_purchase/payment_cancelled.html')
