# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from nasab_users.models import Installer
from .models import Customer
from core.models import Installation, Product

from core.forms import InstallationForm
from .forms import CustomerPhoneForm
from jdatetime import datetime as jdatetime


# صفحه اصلی مشتری - وارد کردن شماره موبایل
def customer_login(request):
    if request.method == 'POST':
        form = CustomerPhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            customer, created = Customer.objects.get_or_create(phone=phone)
            request.session['customer_phone'] = phone
            return redirect('customer_panel')
    else:
        form = CustomerPhoneForm()
    return render(request, 'core_login.html', {'form': form})

# پنل مشتری
def customer_panel(request):
    phone = request.session.get('customer_phone')
    if not phone:
        return redirect('customer_login')

    customer = get_object_or_404(Customer, phone=phone)
    installations = Installation.objects.filter(customer=customer)

    context = {
        'customer': customer,
        'installations': installations,
        'today_jalali': jdatetime.now().strftime('%Y/%m/%d'),
    }
    return render(request, 'user_panel.html', context)
