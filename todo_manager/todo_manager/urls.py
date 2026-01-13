from django.contrib import admin
from django.urls import path, include
from todolist import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", views.custom_login, name="login"),
    path("accounts/logout/", views.custom_logout, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("todolist.urls")),
]
