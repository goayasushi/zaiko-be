from django.contrib import admin
from masters.models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "supplier_code", "phone", "email", "prefecture", "city")
    search_fields = ("name", "supplier_code", "email")
    list_filter = ("prefecture",)


admin.site.register(Supplier, SupplierAdmin)
