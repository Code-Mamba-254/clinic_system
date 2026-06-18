from django import forms
from .models import Consultation


class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation

        fields = [
            "complaint",
            "blood_pressure",
            "temperature",
            "pulse_rate",
            "diagnosis",
            "treatment",
            "prescription",
        ]

        widgets = {
            "complaint": forms.Textarea(attrs={"rows": 2}),
            "diagnosis": forms.Textarea(attrs={"rows": 2}),
            "treatment": forms.Textarea(attrs={"rows": 3}),
            "prescription": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "Write prescription (Rx)..."
            }),
        }