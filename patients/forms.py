from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
           "first_name",
    "last_name",
    "id_number",
    "gender",
    "date_of_birth",
    "phone",
        ]