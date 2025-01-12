from django.shortcuts import render, get_object_or_404
from .models import Product,Bid
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.http import JsonResponse
from django.db.models import Q


@login_required(login_url='login')
def product(request):
    query = request.GET.get('search', '')
    if query:

        products = Product.objects.filter(
            Q(product_name__icontains=query) | Q(description__icontains=query),
            is_available=True
        )
    else:

        products = Product.objects.filter(is_available=True)

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'search_query': query
    }
    return render(request, 'product/product.html', context)

@login_required(login_url='login')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    bids = product.bidplacement_bids.all().order_by('-bid_time')

    profile = get_object_or_404(Profile, user=request.user)
    user_coins = profile.coins

    highest_bid = bids.first()

    context = {
        'product': product,
        'bids': bids,
        'user_coins': user_coins,
        'highest_bid': highest_bid,
    }

    return render(request, 'BidPlacement/product_detail.html', context)



def dashboard(request):
    context = {
        'product_count': Product.objects.count(),
        'products': Product.objects.all(),
    }
    return render(request, 'dashboard.html', context)