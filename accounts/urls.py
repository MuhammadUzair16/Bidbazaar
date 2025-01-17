from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views  # Your views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view-purchase-history/', views.view_purchase_history, name='view_purchase_history'),
    path('manage-account/', views.manage_account, name='manage_account'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
