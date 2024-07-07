from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from coin_purchase.models import Purchase
from django.contrib.auth import get_user_model
from datetime import datetime

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
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password, address=address, dob=dob, phone_number=phone_number )
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uidb64': uid,
                'token': token,
        })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email=' + email)





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


@login_required(login_url='login')
def dashboard(request):
    user = request.user
    purchase_history = Purchase.objects.filter(user=user, successful=True)
    context = {
        'purchase_history': purchase_history,
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

        # Validate and parse the date
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
