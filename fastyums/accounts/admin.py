from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import User, Address


class AddressInline(GenericTabularInline):
    model = Address
    extra = 1
    fields = ['name', 'street', 'city', 'state', 'is_default']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'email', 'username', 'first_name', 'last_name', 'get_city'
    ]

    inlines = [AddressInline]

    @admin.display(description='City')
    def get_city(self, obj):
        # Fetch teh default address, or the first one available
        address = obj.addresses.filter(is_default=True).first() or obj.addresses.first()
        return address.city if address else '-'


admin.site.register(Address)
