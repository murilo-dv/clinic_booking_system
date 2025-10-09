from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .forms import LoginForm, PatientCreationForm, PatientForm
from .models import User, Doctor, Patient
from appointments.models import Appointment

# Create your views here.

def patient_signup(request):
    if request.method == 'POST':
        user_form = PatientCreationForm(request.POST)
        profile_form = PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = PatientCreationForm()
        profile_form = PatientForm()

    return render(request, 'users/patient_signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect based on user role
                if user.role == 'admin':
                    return redirect('/admin/')
                elif user.role == 'doctor':
                    return redirect('doctor_dashboard')
                elif user.role == 'staff':
                    return redirect('staff_dashboard')
                else:  # patient
                    return redirect('patient_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# Dashboard views for different user roles
def patient_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('login')
    
    try:
        patient = Patient.objects.get(user=request.user)
        appointments_patient = Appointment.objects.filter(patient=patient).order_by('date', 'timeslot')
        nextAppointment = Appointment.objects.filter(patient=patient, date__gte=timezone.now().date()).order_by('date', 'timeslot').first()
        total_appointments = Appointment.objects.filter(patient=patient).count()
        context = {
            'nextAppointment': nextAppointment,
            'total_appointments': total_appointments,
            'appointments_patient': appointments_patient,
        }
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please contact administrator.')
        context = {
            'nextAppointment': None,
            'total_appointments': 0,
            'appointments_patient': [],
        }
    
    return render(request, 'dashboard/patient_dashboard.html', context)

def doctor_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('login')
    
    try:
        doctor = Doctor.objects.get(user=request.user)
        
        todayAppointments = Appointment.objects.filter(doctor=doctor, date=timezone.now().date()).count()
        appointments_doctor = Appointment.objects.filter(doctor=doctor).order_by('date', 'timeslot')
        
        weekAppointments = Appointment.objects.filter(
            doctor=doctor,
            date__gte=timezone.now().date(),
            date__lt=timezone.now().date() + timezone.timedelta(days=7)
        ).count()
        
        monthAppointments = Appointment.objects.filter(
            doctor=doctor,
            date__gte=timezone.now().date(),
            date__lt=timezone.now().date() + timezone.timedelta(days=30)
        ).count()
        
        # Get next upcoming appointment
        next_patient_appointment = Appointment.objects.filter(
            doctor=doctor,
            date__gte=timezone.now().date()
        ).order_by('date', 'timeslot').first()
        
        # Count total appointments
        total_appointments = appointments_doctor.count()
        
        context = {
            'appointments_doctor': appointments_doctor,
            'next_patient_appointment': next_patient_appointment,
            'total_appointments': total_appointments,
            'todayAppointments': todayAppointments,
            'weekAppointments': weekAppointments,
            'monthAppointments': monthAppointments,
        }
        
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please contact administrator.')
        context = {
            'appointments_doctor': [],
            'next_patient_appointment': None,
            'total_appointments': 0,
        }
    
    return render(request, 'dashboard/doctor_dashboard.html', context)

def staff_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'staff':
        messages.error(request, 'Access denied.')
        return redirect('login')
    return render(request, 'dashboard/staff_dashboard.html')