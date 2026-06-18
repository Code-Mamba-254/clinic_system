from django.db import models
from django.conf import settings

from patients.models import Patient


class Consultation(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="consultations"
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    complaint = models.TextField()

    blood_pressure = models.CharField(
        max_length=20,
        blank=True
    )

    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )

    pulse_rate = models.IntegerField(
        null=True,
        blank=True
    )

    investigation = models.TextField(blank=True)

    diagnosis = models.TextField(blank=True)

    treatment = models.TextField(blank=True)

    remarks = models.TextField(blank=True)
    prescription = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f"{self.patient.patient_number} - {self.created_at.date()}"