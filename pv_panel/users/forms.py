# forms.py
from django import forms
from core.models import Installation
from users.models import Customer


class CustomerPhoneForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={'placeholder': '09123456789', 'class': 'form-control'})
    )
