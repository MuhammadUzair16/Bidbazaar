from django.utils.timezone import now
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Bid
from product.models import Product
from accounts.models import Profile
import random
from django.db.models import Sum
from django.utils import timezone

AI_NAMES = ["Uzair", "Moeen", "Salman", "Atif", "Osama"]

def ai_place_bid(product):
    ai_name = random.choice(AI_NAMES)
    bid_amount = 1

    total_user_bids = product.bidplacement_bids.filter(ai_name__isnull=True).aggregate(total_bid=Sum('bid_amount'))['total_bid'] or 0

    if total_user_bids >= product.price:
        print(f"AI will not place a bid: User bids have reached or exceeded the product price.")
        return None


    bid = Bid.objects.create(
        product=product,
        ai_name=ai_name,
        bid_amount=bid_amount,
        bid_time=timezone.now(),
    )

    print(f"AI placed a bid: {bid_amount} coins with {ai_name} on {product.product_name}")
    return bid

def ai_bid_logic(product):
    actual_price = product.price

    total_user_bids = product.bidplacement_bids.filter(ai_name__isnull=True).aggregate(total_bid=Sum('bid_amount'))['total_bid'] or 0

    if total_user_bids >= actual_price:
        print(f"Total user bids ({total_user_bids}) reached or exceeded product price ({actual_price}). AI will not place a bid.")
        return None


    last_bid = product.bidplacement_bids.order_by('-bid_time').first()

    if last_bid and (now() - last_bid.bid_time).seconds <= 5 and last_bid.user is not None:
        print(f"A real user placed a bid in the last 5 seconds. AI will not place a bid.")
        return None


    print(f"AI is placing a bid. Total user bids: {total_user_bids}, Actual price: {actual_price}")
    return ai_place_bid(product)



def check_winner(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        highest_bid = product.bidplacement_bids.order_by('-bid_amount', '-bid_time').first()

        if highest_bid:
            winner = highest_bid.user if highest_bid.user else None
            product.winner = winner
            product.is_auction_ended = True
            product.save()

            winner_name = f"{winner.first_name} {winner.last_name}" if winner else highest_bid.ai_name

            return JsonResponse({
                'success': True,
                'winner': {
                    'name': winner_name,
                    'bid_amount': highest_bid.bid_amount,
                },
                'message': 'Auction ended successfully.'
            })
        else:
            product.is_auction_ended = True
            product.save()
            return JsonResponse({'success': True, 'message': 'Auction ended with no bids.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})



@staff_member_required
def ai_bid_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        bid = ai_bid_logic(product)
        if bid:
            return JsonResponse({'success': True, 'message': 'AI bid placed successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'AI bid not placed.'})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def product_detail(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    profile = get_object_or_404(Profile, user=request.user)
    user_coins = profile.coins
    bids = product.bids.all().order_by('-bid_time')
    highest_bid = bids.first()


    current_time = now()
    time_left = product.auction_end_time - current_time
    if time_left.total_seconds() <= 0:
        winner = check_winner(product)

    context = {
        'product': product,
        'highest_bid': highest_bid,
        'bids': bids,
        'user_coins': user_coins,
        'time_left': max(0, time_left.total_seconds()),
    }

    return render(request, 'BidPlacement/product_detail.html', context)


@login_required
def place_bid(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        profile = get_object_or_404(Profile, user=request.user)

        if profile.coins >= 1:
            profile.coins -= 0
            profile.save()

            Bid.objects.create(product=product, user=request.user, bid_amount=1, bid_time=now())
            return JsonResponse({'success': True, 'message': 'Bid placed successfully!'})

        return JsonResponse({'success': False, 'message': 'Not enough coins.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@staff_member_required
def end_auction(request, product_id):

    try:
        product = get_object_or_404(Product, id=product_id)
        product.is_auction_ended = True
        product.save()


        return check_winner(request, product_id)

    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def get_highest_bid(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    bids = product.bidplacement_bids.all().order_by('-bid_time').values('user__first_name', 'ai_name', 'bid_amount', 'bid_time')
    return JsonResponse({'bids': list(bids)})

def product_list(request):

    products = Product.objects.all()
    return render(request, 'product/product.html', {'products': products})

@login_required
def bidding_history(request):

    user_bids = Bid.objects.filter(user=request.user).select_related('product')

    return render(request, 'BidPlacement/bidding_history.html', {'user_bids': user_bids})
