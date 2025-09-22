from django import forms
from .models import User, Patient
from django.contrib.auth.forms import UserCreationForm


class PatientCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'  # Set role to patient
        if commit:
            user.save()
        return user

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user', 'status']