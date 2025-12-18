# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from nasab_users.models import Installer
from .models import Customer
from core.models import Installation, Product

from core.forms import InstallationForm
from .forms import CustomerPhoneForm
import jdatetime

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

def customer_panel(request):
    phone = request.session.get('customer_phone')
    if not phone:
        return redirect('customer_login')

    customer = get_object_or_404(Customer, phone=phone)
    installations = Installation.objects.filter(customer=customer).prefetch_related('products').order_by('-installation_date')

    # Get warranty information for all installations
    all_warranty_info = []
    for installation in installations:
        warranty_info = installation.get_product_warranty_info()
        all_warranty_info.extend(warranty_info)

    context = {
        'customer': customer,
        'installations': installations,
        'all_warranty_info': all_warranty_info,
        'today_jalali': jdatetime.datetime.now().strftime('%Y/%m/%d'),
    }
    return render(request, 'user_panel.html', context)