# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import  Installer
from core.models import Installation, Product
from users.models import Customer
from core.forms import InstallationForm
from users.forms import CustomerPhoneForm
from jdatetime import datetime as jdatetime
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _


def installer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # بررسی اینکه این کاربر نصاب باشد
            if hasattr(user, "installer"):
                login(request, user)
                return redirect("installer_panel")
            else:
                messages.error(request, _("این حساب متعلق به نصاب نیست!"))
        else:
            messages.error(request, _("نام کاربری یا رمز عبور اشتباه است."))

    return render(request, "installer_login.html")
    


@login_required
def installer_logout(request):
    logout(request)
    return redirect("installer_login")


@login_required
def installer_panel(request):
    if not hasattr(request.user, "installer"):
        return redirect("installer_login")

    installer = request.user.installer
    installations = Installation.objects.filter(installer=installer)
    products = Product.objects.all()  # لیست محصولات برای فرم

    if request.method == "POST":
        customer_phone = request.POST.get("customer_phone")
        product_ids = request.POST.getlist("product_id")  # ← توجه: لیست محصول‌ها
        notes = request.POST.get("notes")
        product_count = request.POST.get("product_count")

        # پیدا کردن مشتری
        try:
            customer = Customer.objects.get(phone=customer_phone)
        except Customer.DoesNotExist:
            messages.error(request, _("مشتری با این شماره پیدا نشد!"))
            return redirect("installer_panel")

        # ایجاد نصب جدید
        installation = Installation.objects.create(
            customer=customer,
            installer=installer,
            count = product_count,
            notes=notes
        )

        # اضافه کردن محصولات انتخاب شده
        selected_products = Product.objects.filter(id__in=product_ids)
        installation.products.set(selected_products)

        messages.success(request, _("نصب با موفقیت ثبت شد"))
        return redirect("installer_panel")

    return render(request, "installer_panel.html", {
        "installer": installer,
        "installations": installations,
        "products": products,
    })




