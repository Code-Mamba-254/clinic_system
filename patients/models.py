from django.db import models
from datetime import date


class Patient(models.Model):

    id_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text="National ID or Passport Number"
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other"),
        ]
    )

    date_of_birth = models.DateField()

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False
    )

    phone = models.CharField(max_length=20, blank=True)

    patient_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # ----------------------------
    # AUTO AGE CALCULATION
    # ----------------------------
    def calculate_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    # ----------------------------
    # AUTO PATIENT NUMBER
    # ----------------------------
    def save(self, *args, **kwargs):

        # Auto age update
        if self.date_of_birth:
            self.age = self.calculate_age()

        # Auto patient number (simple fallback if not already set)
        if not self.patient_number:
            last = Patient.objects.order_by("-id").first()
            next_id = 1 if not last else last.id + 1

            year = date.today().year
            self.patient_number = f"PT-{year}-{next_id:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_number} - {self.first_name} {self.last_name}"