from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.shortcuts import render


def role_select(request):
    return render(request, "registration/role_select.html")


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # First page: role selection
    path("", role_select, name="role_select"),

    # Auth
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("redirect/", user_views.role_redirect, name="role_redirect"),

    # Apps
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
]