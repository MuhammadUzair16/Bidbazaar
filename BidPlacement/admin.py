from django.contrib import admin
from .models import Bid

class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'bid_amount', 'bid_time')
    search_fields = ('user', 'product__product_name')
    list_filter = ('product',)

admin.site.register(Bid, BidAdmin)

