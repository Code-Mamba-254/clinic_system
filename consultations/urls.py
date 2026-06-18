from django.urls import path
from . import views

urlpatterns = [
    path(
        "new/<int:patient_id>/",
        views.create_consultation,
        name="create_consultation"
    ),
   
    path("print/<int:pk>/", views.consultation_print, name="consultation_print"),
path("pdf/<int:pk>/", views.consultation_pdf, name="consultation_pdf"),
]