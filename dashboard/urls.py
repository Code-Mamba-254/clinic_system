from django.urls import path
from . import views

urlpatterns = [
    path("doctor/", views.doctor_dashboard, name="doctor_dashboard"),
    path("reception/", views.reception_dashboard, name="reception_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("search/", views.patient_search_api, name="patient_search_api"),
    path("start/", views.start_consultation, name="start_consultation"),
]