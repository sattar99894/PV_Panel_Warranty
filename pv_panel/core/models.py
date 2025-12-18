from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from nasab_users.models import Installer
from users.models import Customer
import jdatetime
from django.utils.translation import gettext_lazy as _



class Product(models.Model):
    serial_number = models.CharField(max_length=50, unique=True, verbose_name=_("شماره سریال"))
    model_name = models.CharField(max_length=100, verbose_name=_("نام مدل"))
    warranty_months = models.PositiveIntegerField(default=12, verbose_name=_("مدت گارانتی (ماه)"))
    purchase_date = models.DateField(null=True, blank=True, verbose_name=_("تاریخ خرید"))

    @property
    def warranty_end_date(self):
        """Returns warranty end date based on installation date"""
        if hasattr(self, 'installation') and self.installation.installation_date:
            return self.installation.installation_date + timezone.timedelta(
                days=self.warranty_months * 30
            )
        return None

    @property
    def remaining_days(self):
        """Returns remaining warranty days"""
        if self.warranty_end_date:
            delta = self.warranty_end_date - timezone.now()
            return max(0, delta.days)
        return 0

    @property
    def warranty_status(self):
        """Returns warranty status"""
        if self.remaining_days > 0:
            return "active"
        return "expired"

    def __str__(self):
        return f"{self.model_name} - {self.serial_number}"


class Installation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    installer = models.ForeignKey(Installer, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(max_length=10, verbose_name=_("تعداد محصولات"))
    installation_date = models.DateTimeField(default=timezone.now, verbose_name=_("تاریخ نصب"))
    notes = models.TextField(blank=True, verbose_name=_("توضیحات"))

    def get_product_warranty_info(self):
        """Returns warranty information for all products in this installation"""
        warranty_info = []
        installer = self.installer
        count = self.count
        for product in self.products.all():
            end_date = self.installation_date + timezone.timedelta(
                days=product.warranty_months * 30
            )
            remaining_days = max(0, (end_date - timezone.now()).days)
                # تبدیل تاریخ نصب به جلالی
            jalali_installation_date = jdatetime.datetime.fromgregorian(datetime=self.installation_date)
            warranty_info.append({
                'product': product,
                'warranty_end_date': end_date,
                'remaining_days': remaining_days,
                "installer" : installer,
                "count" : count ,
                'status': 'active' if remaining_days > 0 else 'expired',
                'jalali_end_date': jdatetime.datetime.fromgregorian(datetime=end_date),
                'jalali_installation_date': jalali_installation_date.strftime('%Y/%m/%d'),  # ← اضافه شده

            })
        return warranty_info
    

    def __str__(self):
        return f"نصب {self.customer} - {self.products.count()} محصول"
    