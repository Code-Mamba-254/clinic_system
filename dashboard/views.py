from django.shortcuts import render
from patients.models import Patient
from consultations.models import Consultation
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from patients.models import Patient
from consultations.models import Consultation
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from core.permissions import doctor_required, receptionist_required, admin_required

@login_required
def role_router(request):

    user = request.user

    # Admin (superuser OR Admin group)
    if user.is_superuser or user.groups.filter(name="Admin").exists():
        return redirect("admin_dashboard")

    # Doctor
    if user.groups.filter(name="Doctor").exists():
        return redirect("doctor_dashboard")

    # Receptionist
    if user.groups.filter(name="Receptionist").exists():
        return redirect("reception_dashboard")

    # fallback
    return redirect("login")

@login_required
@doctor_required
def doctor_dashboard(request):

    my_consultations = Consultation.objects.filter(
        doctor=request.user
    ).order_by("-created_at")[:10]

    return render(request, "dashboard/doctor_dashboard.html", {
        "my_consultations": my_consultations
    })
@login_required
@receptionist_required
def reception_dashboard(request):

    patients = Patient.objects.order_by("-created_at")[:10]

    return render(request, "dashboard/reception_dashboard.html", {
        "patients": patients
    })

@login_required
@admin_required
def admin_dashboard(request):

    return render(request, "dashboard/admin_dashboard.html")
@login_required
def dashboard(request):

    today = timezone.now().date()

    patients_count = Patient.objects.count()

    consultations_today = Consultation.objects.filter(
        created_at__date=today
    ).count()

    my_consultations = Consultation.objects.filter(
        doctor=request.user
    ).order_by("-created_at")[:5]

    recent_patients = Patient.objects.order_by("-created_at")[:5]

    return render(request, "dashboard/dashboard.html", {
        "patients_count": patients_count,
        "consultations_today": consultations_today,
        "my_consultations": my_consultations,
        "recent_patients": recent_patients,
    })

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