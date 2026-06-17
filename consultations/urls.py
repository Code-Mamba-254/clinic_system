from django.urls import path
from . import views

urlpatterns = [
    path(
        "new/<int:patient_id>/",
        views.create_consultation,
        name="create_consultation"
    ),
]