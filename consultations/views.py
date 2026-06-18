from django.shortcuts import render, redirect, get_object_or_404

from patients.models import Patient
from django.contrib.auth.decorators import login_required
from .models import Consultation
from .forms import ConsultationForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from core.permissions import doctor_required
from django.contrib import messages
@login_required


@doctor_required
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
            consultation.prescription = form.cleaned_data["prescription"]
            consultation.save()
            messages.success(request, "Consultation saved successfully.")
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
def prescription_print(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)

    return render(request, "consultations/prescription_print.html", {
        "c": consultation
    })   
def consultation_print(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)

    return render(request, "consultations/consultation_print.html", {
        "c": consultation
    })

def consultation_pdf(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="clinic_note_{pk}.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 800, "CLINIC MEDICAL NOTE")

    p.setFont("Helvetica", 11)

    p.drawString(50, 770, f"Patient: {consultation.patient.first_name} {consultation.patient.last_name}")
    p.drawString(50, 755, f"Patient No: {consultation.patient.patient_number}")
    p.drawString(50, 740, f"Age/Gender: {consultation.patient.age} / {consultation.patient.gender}")

    p.drawString(50, 710, f"Doctor: {consultation.doctor.username}")
    p.drawString(50, 695, f"Date: {consultation.created_at}")

    p.drawString(50, 660, "Complaint:")
    p.drawString(70, 645, consultation.complaint[:100])

    p.drawString(50, 620, "Diagnosis:")
    p.drawString(70, 605, consultation.diagnosis[:100])

    p.drawString(50, 580, "Treatment:")
    p.drawString(70, 565, consultation.treatment[:100])

    p.drawString(50, 540, "Prescription:")
    text = p.beginText(70, 525)
    text.textLines(consultation.prescription or "")
    p.drawText(text)

    p.showPage()
    p.save()

    return response