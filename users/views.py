from django.shortcuts import render, redirect
from .forms import PatientCreationForm, PatientForm
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