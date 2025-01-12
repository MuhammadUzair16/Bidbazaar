from django.urls import path
from . import views

app_name = 'rewards'

urlpatterns = [
    path('distribute_rewards/<int:product_id>/', views.distribute_rewards, name='distribute_rewards'),
    path('redeem_rewards/<int:points_to_redeem>/', views.redeem_rewards, name='redeem_rewards'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),

]
