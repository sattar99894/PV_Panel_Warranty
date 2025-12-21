# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import  Installer
from core.models import Installation
from users.models import Customer
from users.forms import CustomerPhoneForm
from jdatetime import datetime as jdatetime
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from core.forms import InstallationForm, InstallationImageFormSet


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
    installer = request.user.installer
    installations = Installation.objects.filter(installer=installer)

    if request.method == "POST":
        form = InstallationForm(request.POST)
        formset = InstallationImageFormSet(request.POST, request.FILES)  # ارسال فایل‌ها

        # چاپ وضعیت فرم و فرم‌ست
        print("Form is valid:", form.is_valid())  # چاپ وضعیت اعتبارسنجی فرم
        print("Formset is valid:", formset.is_valid())  # چاپ وضعیت اعتبارسنجی فرم‌ست

        # چاپ ارورهای فرم و فرم‌ست
        if not form.is_valid():
            print("Form errors:", form.errors)  # چاپ ارورهای فرم

        if not formset.is_valid():
            print("Formset errors:", formset.errors)  # چاپ ارورهای فرم‌ست

        if form.is_valid() and formset.is_valid():
            installation = form.save(commit=False)
            installation.installer = installer
            installation.save()  # ذخیره نصب
            formset.instance = installation
            formset.save()  # ذخیره تصاویر نصب
            messages.success(request, "نصب با موفقیت ثبت شد.")
            return redirect('installer_panel')
        else:

            messages.error(request, "لطفاً فرم‌ها را به درستی پر کنید.")
            # در صورت عدم اعتبارسنجی صحیح فرم‌ها، چاپ ارورهای بیشتری
            print("Form errors after submission:", form.errors)
            print("Formset errors after submission:", formset.errors)
    
    else:
        form = InstallationForm()
        formset = InstallationImageFormSet()

    context = {
        'form': form,
        'formset': formset,
        'installations': installations,
    }

    return render(request, 'installer_panel.html', context)
