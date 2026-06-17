from django.shortcuts import render
from patients.models import Patient
from consultations.models import Consultation
from django.db.models import Q
from django.http import JsonResponse


def patient_search_api(request):

    query = request.GET.get("q", "")

    patients = Patient.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(phone__icontains=query) |
        Q(patient_number__icontains=query)
    )[:10]

    data = [
        {
            "id": p.id,
            "patient_number": p.patient_number,
            "name": f"{p.first_name} {p.last_name}",
            "phone": p.phone,
        }
        for p in patients
    ]

    return JsonResponse(data, safe=False)


def dashboard(request):

    patients = Patient.objects.all().order_by("-id")[:5]
    consultations = Consultation.objects.all().order_by("-created_at")[:5]

    context = {
        "total_patients": Patient.objects.count(),
        "total_consultations": Consultation.objects.count(),
        "recent_patients": patients,
        "recent_consultations": consultations,
    }

    return render(request, "dashboard/home.html", context)


def start_consultation(request):

    query = request.GET.get("q")
    patients = []

    if query:
        patients = Patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(patient_number__icontains=query)
        )

    return render(
        request,
        "dashboard/start_consultation.html",
        {"patients": patients, "query": query}
    )