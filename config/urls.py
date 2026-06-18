from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from dashboard.views import role_router

urlpatterns = [
    # 🧠 ROOT → ROLE ROUTER (MOST IMPORTANT LINE)
    path("", role_router, name="role_router"),

    # Admin panel
    path("admin/", admin.site.urls),

    # Apps
    path("patients/", include("patients.urls")),
    path("consultations/", include("consultations.urls")),
    path("dashboard/", include("dashboard.urls")),

    # Auth
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]