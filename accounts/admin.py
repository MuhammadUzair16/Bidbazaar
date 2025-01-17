from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,Profile

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class MyAccountAdmin(AccountAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address', 'city', 'state', 'country')
    list_display_links = ('name', 'email')
    readonly_fields = ('phone_number', 'address', 'city', 'state', 'country')
    ordering = ('name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)
