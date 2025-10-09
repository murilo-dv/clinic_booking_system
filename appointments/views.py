from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django import forms
from .forms import AppointmentForm
from .models import Appointment
from users.models import Patient, Doctor

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


@login_required
def appointments_list(request):
    """View to list appointments based on user role"""
    from datetime import date
    
    if request.user.role == 'doctor':
        try:
            doctor = Doctor.objects.get(user=request.user)
            appointments = Appointment.objects.filter(doctor=doctor).order_by('-date', '-timeslot')
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
            return redirect('doctor_dashboard')
    elif request.user.role == 'patient':
        try:
            patient = Patient.objects.get(user=request.user)
            appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-timeslot')
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
            return redirect('patient_dashboard')
    elif request.user.role == 'staff' or request.user.is_superuser:
        appointments = Appointment.objects.all().order_by('-date', '-timeslot')
    else:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    return render(request, 'appointments/appointments_list.html', {
        'appointments': appointments,
        'today': date.today()
    })


@login_required
def appointment_detail(request, appointment_id):
    """View to show appointment details"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user has permission to view this appointment
    if request.user.role == 'doctor':
        try:
            doctor = Doctor.objects.get(user=request.user)
            if appointment.doctor != doctor:
                messages.error(request, 'You can only view your own appointments.')
                return redirect('appointments_list')
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
            return redirect('doctor_dashboard')
    elif request.user.role == 'patient':
        try:
            patient = Patient.objects.get(user=request.user)
            if appointment.patient != patient:
                messages.error(request, 'You can only view your own appointments.')
                return redirect('appointments_list')
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
            return redirect('patient_dashboard')
    elif not (request.user.role == 'staff' or request.user.is_superuser):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    from datetime import date
    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment,
        'today': date.today()
    })


@login_required
def appointment_update(request, appointment_id):
    """View to update appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check permissions
    can_edit = False
    if request.user.role == 'doctor':
        try:
            doctor = Doctor.objects.get(user=request.user)
            can_edit = appointment.doctor == doctor
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
            return redirect('doctor_dashboard')
    elif request.user.role == 'patient':
        try:
            patient = Patient.objects.get(user=request.user)
            can_edit = appointment.patient == patient
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
            return redirect('patient_dashboard')
    elif request.user.role == 'staff' or request.user.is_superuser:
        can_edit = True
    
    if not can_edit:
        messages.error(request, 'You do not have permission to edit this appointment.')
        return redirect('appointments_list')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            updated_appointment = form.save(commit=False)
            
            # Check if the new time slot is available (excluding current appointment)
            existing_appointment = Appointment.objects.filter(
                doctor=updated_appointment.doctor,
                date=updated_appointment.date,
                timeslot=updated_appointment.timeslot
            ).exclude(id=appointment.id).exists()
            
            if existing_appointment:
                messages.error(request, 'This time slot is already booked. Please choose another time.')
                return render(request, 'appointments/appointment_form.html', {
                    'form': form, 
                    'appointment': appointment,
                    'action': 'Update'
                })
            
            updated_appointment.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment_detail', appointment_id=appointment.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentForm(instance=appointment)
        
        # Restrict form fields based on user role
        if request.user.role == 'patient':
            form.fields['patient'].widget = forms.HiddenInput()
            form.fields['doctor'].widget.attrs['readonly'] = True
    
    return render(request, 'appointments/appointment_form.html', {
        'form': form, 
        'appointment': appointment,
        'action': 'Update'
    })


@login_required
def appointment_delete(request, appointment_id):
    """View to delete appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check permissions
    can_delete = False
    if request.user.role == 'doctor':
        try:
            doctor = Doctor.objects.get(user=request.user)
            can_delete = appointment.doctor == doctor
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
            return redirect('doctor_dashboard')
    elif request.user.role == 'patient':
        try:
            patient = Patient.objects.get(user=request.user)
            can_delete = appointment.patient == patient
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
            return redirect('patient_dashboard')
    elif request.user.role == 'staff' or request.user.is_superuser:
        can_delete = True
    
    if not can_delete:
        messages.error(request, 'You do not have permission to delete this appointment.')
        return redirect('appointments_list')
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('appointments_list')
    
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})

