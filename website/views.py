from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

# Create your views here.
def home(request):
    return render(request, "website/home.html")

def about(request):
    return render(request, "website/aboutus.html")

def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Process the form data here
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['message']
            
            # You can save to database, send email, etc.
            # For now, we'll just show a success message
            messages.success(request, f'Thank you {name}! Your message has been sent successfully.')
            return redirect('contact')
    else:
        contact_form = ContactForm()
    
    return render(request, "website/contact.html", {'contact_form': contact_form})

def terms(request):
    return render(request, "website/terms.html")

def privacy(request):
    return render(request, "website/privacy.html")

