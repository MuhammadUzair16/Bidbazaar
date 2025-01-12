from django.contrib import admin
from .models import CoinPackage, Purchase


class CoinPackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'package_version')
    list_filter = ('package_name', 'package_version')
    search_fields = ('package_name', 'package_version')


admin.site.register(CoinPackage)
admin.site.register(Purchase)
