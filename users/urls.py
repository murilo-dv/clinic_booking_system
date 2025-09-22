from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.patient_signup, name='patient_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
]