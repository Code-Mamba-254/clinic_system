from django.shortcuts import render, redirect, get_object_or_404

from patients.models import Patient
from django.contrib.auth.decorators import login_required
from .models import Consultation
from .forms import ConsultationForm
@login_required
def create_consultation(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == "POST":

        form = ConsultationForm(request.POST)

        if form.is_valid():

            consultation = form.save(
                commit=False
            )

            consultation.patient = patient
            consultation.doctor = request.user

            consultation.save()

            return redirect(
                "patient_detail",
                pk=patient.id
            )

    else:
        form = ConsultationForm()

    return render(
        request,
        "consultations/consultation_form.html",
        {
            "patient": patient,
            "form": form
        }
    )