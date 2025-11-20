# warranty/admin.py
from django.contrib import admin
from users.models import Customer
from core.models import  Product, Installation
from .models import Installer


@admin.register(Installer)
class InstallerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'user')
    search_fields = ('full_name', 'user__username')
    ordering = ('id',)
