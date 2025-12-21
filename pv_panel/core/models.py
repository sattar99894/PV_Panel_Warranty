from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from nasab_users.models import Installer
from users.models import Customer
import jdatetime
from uuid import uuid4


def upload_installation_image(instance, filename):
    return f"media"


# models.py
class Installation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    installer = models.ForeignKey(Installer, on_delete=models.SET_NULL, null=True)
    installation_date = models.DateTimeField(default=timezone.now, verbose_name=_("تاریخ نصب"))
    notes = models.TextField(blank=True, verbose_name=_("توضیحات"))

    # فیلدهای جدید برای محصول
    model_name = models.CharField(max_length=100, verbose_name=_("نام مدل"))
    warranty_months = models.PositiveIntegerField(default=12, verbose_name=_("مدت گارانتی (ماه)"))
    serial_number = models.CharField(max_length=50, unique=True, verbose_name=_("شماره سریال"))

    # فیلد آدرس به صورت یک فیلد واحد
    address = models.CharField(max_length=1254, blank=True, null=True, verbose_name=_("آدرس کامل"))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("شهر"))
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("شهرستان"))

    def __str__(self):
        return f"نصب {self.customer} - محصول {self.model_name} با شماره سریال {self.serial_number}"

    def get_product_warranty_info(self):
        """Returns warranty information for the product in this installation"""
        warranty_info = []
        installer = self.installer

        # استفاده از فیلدهای موجود در همین مدل برای اطلاعات محصول
        end_date = self.installation_date + timezone.timedelta(
            days=self.warranty_months * 30
        )
        remaining_days = max(0, (end_date - timezone.now()).days)
        # تبدیل تاریخ نصب به جلالی
        jalali_installation_date = jdatetime.datetime.fromgregorian(datetime=self.installation_date)

        warranty_info.append({
            'model_name': self.model_name,
            'serial_number': self.serial_number,
            'warranty_end_date': end_date,
            'remaining_days': remaining_days,
            'installer': installer,
            'status': 'active' if remaining_days > 0 else 'expired',
            'jalali_end_date': jdatetime.datetime.fromgregorian(datetime=end_date),
            'jalali_installation_date': jalali_installation_date.strftime('%Y/%m/%d'),
        })

        return warranty_info  
    
    @property
    def jalali_end_date(self):
        end_date = self.installation_date + timezone.timedelta(
            days=self.warranty_months * 30
        )
        # تبدیل تاریخ نصب به جلالی
        return jdatetime.datetime.fromgregorian(datetime=end_date).strftime('%Y/%m/%d')
    
    @property
    def jalali_installation_date(self):
        end_date = self.installation_date + timezone.timedelta(
            days=self.warranty_months * 30
        )
        # تبدیل تاریخ نصب به جلالی
        jalali_installation_date = jdatetime.datetime.fromgregorian(datetime=self.installation_date)
        return jalali_installation_date.strftime('%Y/%m/%d')



    @property
    def warranty_end_date(self):
        """Returns warranty end date based on installation date"""
        # اگر تاریخ نصب وجود داشته باشد، تاریخ پایان گارانتی محاسبه می‌شود
        if self.installation_date:
            # افزودن ماه‌های گارانتی به تاریخ نصب
            return self.installation_date + timezone.timedelta(days=self.warranty_months * 30)
        return None

    @property
    def remaining_days(self):
        """Returns remaining warranty days"""
        # اگر تاریخ پایان گارانتی وجود داشته باشد، روزهای باقی‌مانده محاسبه می‌شود
        if self.warranty_end_date:
            delta = self.warranty_end_date - timezone.now()
            return max(0, delta.days)  # بازگشت 0 اگر زمان باقی‌مانده منفی باشد
        return 0

    @property
    def warranty_status(self):
        """Returns warranty status"""
        # اگر روزهای باقی‌مانده بیشتر از صفر باشد، گارانتی فعال است
        if self.remaining_days > 0:
            return "active"
        return "expired"

    def __str__(self):
        return f"نصب {self.customer} "


class InstallationImage(models.Model):
    installation = models.ForeignKey(Installation, related_name="images", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=upload_installation_image)

