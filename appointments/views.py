from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import AppointmentForm
from .models import Appointment
from users.models import Patient

# Create your views here.

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            # If the user is a patient, automatically assign them
            if request.user.role == 'patient':
                try:
                    patient = Patient.objects.get(user=request.user)
                    appointment.patient = patient
                except Patient.DoesNotExist:
                    messages.error(request, 'Patient profile not found. Please complete your profile first.')
                    return redirect('patient_signup')
            
            # Check if the time slot is already booked
            existing_appointment = Appointment.objects.filter(
                doctor=appointment.doctor,
                date=appointment.date,
                timeslot=appointment.timeslot
            ).exists()
            
            if existing_appointment:
                messages.error(request, 'This time slot is already booked. Please choose another time.')
                return render(request, 'appointments/book_appointment.html', {'form': form})
            
            appointment.save()
            messages.success(request, 'Your appointment has been booked successfully! We will contact you soon.')
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentForm()
        
        # If user is a patient, hide the patient field and pre-select them
        if request.user.role == 'patient':
            try:
                patient = Patient.objects.get(user=request.user)
                form.fields['patient'].initial = patient
                form.fields['patient'].widget = forms.HiddenInput()
            except Patient.DoesNotExist:
                messages.error(request, 'Please complete your patient profile first.')
                return redirect('patient_signup')
    
    return render(request, 'appointments/book_appointment.html', {'form': form})

