from django.contrib import admin

from .models import Address, AddressConnector


class AdminConnectorInline(admin.TabularInline):
    model = AddressConnector


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = [
        "uid",
        "city",
        "country",
        "type",
        "status",
    ]
    list_filter = [
        "type",
        "status",
    ]
    readonly_fields = ["uid", "slug"]
    inlines = [AdminConnectorInline]


@admin.register(AddressConnector)
class AddressConnectorAdmin(admin.ModelAdmin):
    model = AddressConnector
    list_display = [
        "uid",
        "address",
        "patient",
        "doctor",
    ]
    list_filter = ["patient", "doctor", "organization"]
