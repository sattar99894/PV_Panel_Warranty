# warranty/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_login, name='customer_login'),
    path('panel/', views.customer_panel, name='customer_panel'),
]