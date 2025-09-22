import django.forms as forms
from .models import Appointment
from users.models import Doctor, Patient

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["doctor", "patient", "date", "timeslot", "description"]
        labels = {
            "doctor": "Select Doctor",
            "patient": "Patient Name",
            "date": "Appointment Date",
            "timeslot": "Preferred Time",
            "description": "Additional Notes"
        }
        widgets = {
            'doctor': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'required': True
            }),
            'patient': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'required': True
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'required': True
            }),
            'timeslot': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none',
                'placeholder': 'Please describe your symptoms or reason for the appointment...'
            }),
        }
        help_texts = {
            'date': 'Please select your preferred appointment date.',
            'timeslot': 'Choose from available time slots.',
            'description': 'Optional: Provide any additional information that might help the doctor prepare for your visit.',
        }