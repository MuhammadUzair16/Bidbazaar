from django.shortcuts import render
from django.http import JsonResponse
from .models import RewardPool, UserRewardPoints, RewardTransaction
from BidPlacement.models import Product, Bid
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserRewardPoints, RewardTransaction

from django.contrib.auth.decorators import login_required


@login_required
def redeem_rewards(request, points_to_redeem):

    user_reward_points = UserRewardPoints.objects.get(user=request.user)

    if user_reward_points.points < points_to_redeem:
        return JsonResponse({"message": "You don't have enough points to redeem."}, status=400)


    user_reward_points.points -= points_to_redeem
    user_reward_points.save()

    RewardTransaction.objects.create(
        user=request.user,
        points=-points_to_redeem,
        transaction_type='redemption',
        product=None
    )

    return JsonResponse({"message": f"Successfully redeemed {points_to_redeem} points!"})

def allocate_reward_pool(product: Product):

    auction_profit = product.auction_profit
    reward_amount = auction_profit * 0.1


    reward_pool, created = RewardPool.objects.get_or_create(id=1)
    reward_pool.total_amount += reward_amount
    reward_pool.save()

    return reward_amount



@login_required
def distribute_rewards(request, product_id):

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Product not found."}, status=404)

    reward_pool = RewardPool.objects.get(id=1)


    all_bids = Bid.objects.filter(product=product)
    if not all_bids:
        return JsonResponse({"message": "No bids placed for this product."}, status=400)

    # Find the winning bid
    winning_bid = max(all_bids, key=lambda bid: bid.bid_amount)


    winning_user = winning_bid.user


    user_bids = {}
    for bid in all_bids:
        if bid.user not in user_bids:
            user_bids[bid.user] = 0
        user_bids[bid.user] += bid.bid_amount

    for user, total_bid in user_bids.items():
        reward_points = int((total_bid / 10) * 5)
        user_reward, created = UserRewardPoints.objects.get_or_create(user=user)
        user_reward.points += reward_points
        user_reward.save()


        RewardTransaction.objects.create(
            user=user,
            points=reward_points,
            transaction_type='distribution',
            product=product
        )

    winning_user_reward, created = UserRewardPoints.objects.get_or_create(user=winning_user)
    winning_user_reward.points += int((winning_bid.bid_amount / 10) * 5)
    winning_user_reward.save()

    RewardTransaction.objects.create(
        user=winning_user,
        points=int((winning_bid.bid_amount / 10) * 5),
        transaction_type='distribution',
        product=product
    )

    return JsonResponse({"message": f"Reward points distributed successfully. Winner: {winning_user.username}"})

def dashboard(request):

    user = request.user
    try:
        reward_points = UserRewardPoints.objects.get(user=request.user)
    except UserRewardPoints.DoesNotExist:
        reward_points = None

    transactions = RewardTransaction.objects.filter(user=user).order_by('-timestamp')

    return render(request, 'rewards/rewards_points.html', {
        'user': user,
        'reward_points': reward_points,
        'transactions': transactions
    })


def transaction_history(request):
    user = request.user
    transactions = RewardTransaction.objects.filter(user=user).order_by('-timestamp')

    return render(request, 'rewards/transaction_history.html', {
        'transactions': transactions
    })
