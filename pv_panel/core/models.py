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

    def __str__(self):
        return f"{self.model_name} - {self.serial_number}"


class Installation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    installer = models.ForeignKey(Installer, on_delete=models.SET_NULL, null=True)
    installation_date = models.DateTimeField(default=timezone.now, verbose_name=_("تاریخ نصب"))
    notes = models.TextField(blank=True, verbose_name=_("توضیحات"))

    def warranty_end_dates(self):
        """
        برمی‌گرداند دیکشنری از محصول‌ها و تاریخ پایان گارانتی آنها
        """
        end_dates = {}
        for product in self.products.all():
            end_dates[product.id] = self.installation_date + timezone.timedelta(days=product.warranty_months * 30)
        return end_dates

    def remaining_days(self, product):
        """
        روزهای باقی‌مانده برای محصول مشخص
        """
        end = self.installation_date + timezone.timedelta(days=product.warranty_months * 30)
        delta = end - timezone.now()
        return delta.days if delta.days > 0 else 0

    def remaining_days_jalali(self, product):
        """
        روزهای باقی‌مانده به صورت تاریخ جلالی برای محصول مشخص
        """
        end_jalali = jdatetime.fromgregorian(datetime=self.installation_date + timezone.timedelta(days=product.warranty_months * 30))
        today_jalali = jdatetime.now()
        return (end_jalali - today_jalali).days

    def __str__(self):
        return f"نصب {self.customer} - {self.products.count()} محصول"