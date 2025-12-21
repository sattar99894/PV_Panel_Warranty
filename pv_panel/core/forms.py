# forms.py

from django import forms
from .models import Installation
from users.models import Customer
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from .models import InstallationImage 
from django.utils import timezone

# forms.py# forms.py
class InstallationImageForm(forms.ModelForm):
    class Meta:
        model = InstallationImage
        fields = ['image']  # فقط فیلد تصویر

class InstallationForm(forms.ModelForm):
    customer_phone = forms.CharField(max_length=11, label=_("شماره موبایل مشتری"))
    serial_number = forms.CharField(max_length=50, label=_("شماره سریال محصول"))    
    model_name = forms.CharField(max_length=50, label=_("نام مدل محصول"))
    warranty_months = forms.IntegerField(required=True, label=_("مدت گارانتی (ماه"))
    address = forms.CharField(max_length=512, required=False, label=_("آدرس کامل"))
    city = forms.CharField(max_length=100, required=False, label=_("شهر"))
    district = forms.CharField(max_length=100, required=False, label=_("شهرستان"))
    installation_date = forms.DateTimeField(
        initial=timezone.now,
        label=_("تاریخ نصب"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), required=False, label=_("توضیحات"))

    class Meta:
        model = Installation
        fields = ['customer_phone', 'serial_number','model_name', 'address', 'city','warranty_months', 'district', 'installation_date', 'notes']

    def save(self, commit=True):
        installation = super().save(commit=False)
        customer_phone = self.cleaned_data['customer_phone']
        try:
            customer = Customer.objects.get(phone=customer_phone)
            installation.customer = customer  # ارتباط مشتری با نصب
        except Customer.DoesNotExist:
            raise forms.ValidationError("مشتری با این شماره تلفن یافت نشد.")

        if commit:
            installation.save()
        return installation


InstallationImageFormSet = inlineformset_factory(
    Installation,
    InstallationImage,
    form=InstallationImageForm,  # استفاده از فرم اصلاح‌شده
    fields=['image'],  # فقط فیلد تصویر
    extra=3,  # اضافه کردن فرم‌های اضافی برای تصاویر
    can_delete=True,
)