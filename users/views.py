from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, PatientCreationForm, PatientForm
from .models import User

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
            return redirect('login')  # Redirect to login page after successful signup
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
                    return redirect('doctor_dashboard')  # You'll need to create this
                elif user.role == 'staff':
                    return redirect('staff_dashboard')   # You'll need to create this
                else:  # patient
                    return redirect('patient_dashboard') # You'll need to create this
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
    return render(request, 'users/patient_dashboard.html')

def doctor_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('login')
    return render(request, 'users/doctor_dashboard.html')

def staff_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'staff':
        messages.error(request, 'Access denied.')
        return redirect('login')
    return render(request, 'users/staff_dashboard.html')