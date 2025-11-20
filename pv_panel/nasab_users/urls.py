# warranty/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path("login/", views.installer_login, name="installer_login"),
    path("logout/", views.installer_logout, name="installer_logout"),
    path("panel/", views.installer_panel, name="installer_panel"),
]