from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Customer(models.Model):
    phone = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone