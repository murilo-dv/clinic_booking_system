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

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your password'
        })
    )
