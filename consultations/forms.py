from django import forms
from .models import Consultation


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation

        exclude = [
            "patient",
            "doctor",
            "created_at",
        ]