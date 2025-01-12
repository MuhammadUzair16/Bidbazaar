from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from coin_purchase.models import Purchase
from BidPlacement.models import Bid
from product.models import Product
from rewards.models import UserRewardPoints, RewardPool, RewardTransaction
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            dob = form.cleaned_data['dob']
            password = form.cleaned_data['password']
            username = email.split("@")[0]


            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
                address=address,
                dob=dob,
                phone_number=phone_number,
            )
            user.is_active = True
            user.save()

            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('login')

    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Your are now Logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')



@login_required
def dashboard(request):
    purchase_history = Purchase.objects.filter(user=request.user).order_by('-purchase_date')
    purchase_dates = [purchase.purchase_date.strftime('%Y-%m-%d') for purchase in purchase_history]
    purchase_coins = [purchase.amount for purchase in purchase_history]

    bidding_history = Bid.objects.filter(user=request.user).order_by('-bid_time')
    bidding_products = [bid.product.product_name for bid in bidding_history]
    bidding_amounts = [bid.bid_amount for bid in bidding_history]

    try:
        user_rewards = UserRewardPoints.objects.get(user=request.user)
    except UserRewardPoints.DoesNotExist:
        user_rewards = UserRewardPoints.objects.create(user=request.user, points=0)

    # Fetch products won by the user
    won_products = Product.objects.filter(winner=request.user)

    # Get highest bid for each product
    products_with_highest_bids = []
    for product in won_products:
        highest_bid = product.bidplacement_bids.order_by('-bid_amount', '-bid_time').first()
        products_with_highest_bids.append({
            'product': product,
            'highest_bid': highest_bid
        })

    context = {
        'purchase_history': purchase_history,
        'bidding_history': bidding_history,
        'purchase_dates': purchase_dates,
        'purchase_coins': purchase_coins,
        'bidding_products': bidding_products,
        'bidding_amounts': bidding_amounts,
        'user_rewards': user_rewards.points,
        'won_products': products_with_highest_bids,
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required
def view_purchase_history(request):
    user = request.user
    purchase_history = Purchase.objects.filter(user=user, successful=True)
    context = {
        'purchase_history': purchase_history,
    }
    return render(request, 'accounts/view_purchase_history.html', context)


User = get_user_model()

@login_required
def manage_account(request):
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        dob = request.POST.get('dob')

        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.address = address


        try:
            user.dob = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD format.')
            return redirect('manage_account')

        user.save()
        messages.success(request, 'Account details updated successfully.')
        return redirect('manage_account')

    context = {
        'user': request.user,
    }
    return render(request, 'accounts/manage_account.html', context)

from django.db import transaction
from django.core.exceptions import ValidationError

@login_required
def redeem_rewards(request, points_to_redeem):

    try:
        user_points = UserRewardPoints.objects.get(user=request.user)
    except UserRewardPoints.DoesNotExist:
        user_points = UserRewardPoints.objects.create(user=request.user, points=0)

    if user_points.points >= points_to_redeem:
        try:

            with transaction.atomic():

                user_points.points -= points_to_redeem
                user_points.save()


                RewardTransaction.objects.create(
                    user=request.user,
                    points=points_to_redeem,
                    transaction_type='redemption',
                    product=None
                )

            messages.success(request, f"You have successfully redeemed {points_to_redeem} points!")
        except ValidationError as e:
            messages.error(request, f"A validation error occurred: {str(e)}")
        except Exception as e:
            messages.error(request, f"An error occurred while processing your redemption: {str(e)}")
    else:
        messages.error(request, "You don't have enough reward points to redeem.")

    return redirect('dashboard')
