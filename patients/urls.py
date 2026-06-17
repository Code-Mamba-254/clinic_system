from django.urls import path
from . import views

urlpatterns = [
    path("", views.patient_list, name="patient_list"),
    path("new/", views.create_patient, name="create_patient"),
    path("<int:pk>/", views.patient_detail, name="patient_detail"),
]