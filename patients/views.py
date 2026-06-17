from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm
@login_required
def create_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect("patient_detail", pk=patient.id)
    else:
        form = PatientForm()

    return render(request, "patients/patient_form.html", {"form": form})
@login_required
def patient_list(request):
    query = request.GET.get("q")

    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(patient_number__icontains=query)
        )

    return render(request, "patients/patient_list.html", {
        "patients": patients,
        "query": query
    })
@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    consultations = patient.consultations.all().order_by("-created_at")

    return render(request, "patients/patient_detail.html", {
        "patient": patient,
        "consultations": consultations
    })