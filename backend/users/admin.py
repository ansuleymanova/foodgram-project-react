from django.contrib import admin

from .models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',
                    'username', 'email')
    search_fields = ('email', 'username')
    list_filter = ('email', 'username', 'last_name')
    empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'subscriber')


admin.site.register(Subscription, SubscriptionAdmin)
