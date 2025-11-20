# warranty/admin.py
from django.contrib import admin
from .models import Customer
from core.models import  Product, Installation
from nasab_users.models import Installer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')
    search_fields = ('phone',)
    ordering = ('id',)

