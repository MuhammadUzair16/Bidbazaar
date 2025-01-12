from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('product/', include('product.urls')),
    path('accounts/', include('accounts.urls')),
    path('coin_purchase/', include('coin_purchase.urls')),
    path('bid/', include('BidPlacement.urls')),
    path('rewards/', include('rewards.urls')),


   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
