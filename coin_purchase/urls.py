# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('buy-now/', views.buy_now, name='buy_now'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
]


