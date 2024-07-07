from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def product(request):
    products = Product.objects.all().filter(is_available=True)
    product_count = products.count()

    context = {

        'products': products,
        'product_count': product_count,
    }
    return render(request, 'product/product.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/product_detail.html', {'product': product})




def dashboard(request):

    context = {
        'product_count': 10,
        'products': Product.objects.all(),
    }
    return render(request, 'dashboard.html', context)

