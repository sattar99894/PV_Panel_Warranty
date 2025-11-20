# forms.py
from django import forms
from .models import Installation, Product
from users.models import Customer


class InstallationForm(forms.ModelForm):
    customer_phone = forms.CharField(max_length=11, label="شماره موبایل مشتری")
    serial_number = forms.CharField(max_length=50, label="شماره سریال محصول")

    class Meta:
        model = Installation
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, installer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.installer = installer

    def clean_customer_phone(self):
        phone = self.cleaned_data['customer_phone']
        customer, _ = Customer.objects.get_or_create(phone=phone)
        return customer

    def clean_serial_number(self):
        serial = self.cleaned_data['serial_number']
        try:
            product = Product.objects.get(serial_number=serial)
            if Installation.objects.filter(product=product).exists():
                raise forms.ValidationError("این محصول قبلاً نصب شده است.")
            return product
        except Product.DoesNotExist:
            raise forms.ValidationError("شماره سریال یافت نشد.")

    def save(self, commit=True):
        installation = super().save(commit=False)
        installation.customer = self.cleaned_data['customer_phone']
        installation.product = self.cleaned_data['serial_number']
        if commit:
            installation.save()
        return installation