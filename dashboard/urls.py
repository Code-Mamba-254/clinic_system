from django.urls import path
from .views import dashboard, start_consultation,patient_search_api

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("start-consultation/", start_consultation, name="start_consultation"),
    path("api/patients/", patient_search_api, name="patient_search_api"),
]