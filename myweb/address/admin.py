from django.contrib import admin
from address.models import Address

class AddressAdmin(admin.ModelAdmin):
    list_display=('name','tel','email','address')

admin.site.register(Address, AddressAdmin)
