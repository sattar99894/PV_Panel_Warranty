# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer
from core.models import Installation

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

import jdatetime

def customer_panel(request):
    # فرض می‌کنیم که کاربر وارد شده باشد
    phone = request.session.get('customer_phone')
    if not phone:
        return redirect('customer_login')

    customer = get_object_or_404(Customer, phone=phone)

    # بارگذاری نصب‌ها و اطلاعات گارانتی
    installations = Installation.objects.filter(customer=customer).order_by('-installation_date')

    # تبدیل تاریخ‌ها به جلالی
    for installation in installations:
        warranty_info = installation.get_product_warranty_info()
        for item in warranty_info:
            # اضافه کردن تاریخ شمسی به هر گارانتی
            item['jalali_installation_date'] = jdatetime.datetime.fromgregorian(datetime=installation.installation_date).strftime('%Y/%m/%d')
            item['jalali_end_date'] = jdatetime.datetime.fromgregorian(datetime=item['warranty_end_date']).strftime('%Y/%m/%d')

    context = {
        'customer': customer,
        'installations': installations
    }

    return render(request, 'user_panel.html', context)
