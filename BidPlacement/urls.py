from django.urls import path
from . import views

app_name = 'BidPlacement'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('place-bid/<int:product_id>/', views.place_bid, name='place_bid'),
    path('bidding_history/', views.bidding_history, name='bidding_history'),
    path('check-winner/<int:product_id>/', views.check_winner, name='check_winner'),
    path('get-highest-bid/<int:product_id>/', views.get_highest_bid, name='get_highest_bid'),
    path('end-auction/<int:product_id>/', views.end_auction, name='end_auction'),
    path('ai_bid/<int:product_id>/', views.ai_bid_view, name='ai_place_bid'),
]
