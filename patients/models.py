from django.db import models
from django.utils.timezone import now


def generate_patient_number():
    year = now().year

    last_patient = Patient.objects.filter(
        patient_number__startswith=f"PT-{year}"
    ).order_by("id").last()

    if last_patient and last_patient.patient_number:
        last_number = int(last_patient.patient_number.split("-")[-1])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"PT-{year}-{new_number:06d}"


class Patient(models.Model):
    patient_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    gender = models.CharField(
        max_length=10
    )

    date_of_birth = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.patient_number:
            self.patient_number = generate_patient_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_number} - {self.first_name} {self.last_name}"