# warranty/admin.py
from django.contrib import admin
from users.models import Customer
from .models import  Product, Installation
from nasab_users.models import Installer



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "model_name", "serial_number", "warranty_months", "purchase_date")
    search_fields = ("model_name", "serial_number")
    list_filter = ("warranty_months",)
    ordering = ("id",)


@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'installer', 'display_products', 'installation_date')

    def display_products(self, obj):
        return ", ".join([str(p) for p in obj.products.all()])
    display_products.short_description = 'محصولات'

