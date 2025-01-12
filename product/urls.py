
from django.urls import path
from . import views

urlpatterns = [
    path('product_details/<int:product_id>/', views.product_detail, name='product_detail'),
    path('', views.product, name='product'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
