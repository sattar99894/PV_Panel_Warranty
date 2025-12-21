# admin.py
from django.contrib import admin
from .models import  Installation
from django.utils.translation import gettext_lazy as _
from .models import Installation, InstallationImage

class InstallationImageInline(admin.TabularInline):
    model = InstallationImage
    extra = 1  # تعداد عکس‌های اضافی که در فرم جدید نمایش داده شود

class InstallationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'model_name', 'serial_number', 'installation_date', 'warranty_end_date', 'remaining_days']
    search_fields = ('customer__name', 'serial_number', 'model_name')
    list_filter = ['installation_date']
    
    # اضافه کردن نصب‌ها به صورت خطی در پنل مدیریت
    inlines = [InstallationImageInline]
    
    # نمایش تصاویر در داخل لیست نصب‌ها
    readonly_fields = ['get_images']  # برای نمایش تصاویر در نمای readonly

    def get_images(self, obj):
        """نمایش تصاویر نصب‌ها در پنل ادمین"""
        images = obj.images.all()
        return ", ".join([f'<img src="{image.image.url}" width="50" height="50" />' for image in images])  # نمایش تصاویر به صورت کوچکتر
    get_images.allow_tags = True
    get_images.short_description = 'تصاویر'

# ثبت مدل‌ها در پنل ادمین
admin.site.register(Installation, InstallationAdmin)
admin.site.register(InstallationImage)

