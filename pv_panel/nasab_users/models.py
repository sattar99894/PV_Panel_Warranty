
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Installer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, unique=True)
    code = models.CharField(max_length=20, unique=True, help_text=_("کد نصب‌کننده"))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} ({self.code})"
    