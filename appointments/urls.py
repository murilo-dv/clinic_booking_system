from django.urls import path
from . import views

urlpatterns = [
    path("book/", views.book_appointment, name="book_appointment"),
    path("", views.appointments_list, name="appointments_list"),
    path("<int:appointment_id>/", views.appointment_detail, name="appointment_detail"),
    path("<int:appointment_id>/edit/", views.appointment_update, name="appointment_update"),
    path("<int:appointment_id>/delete/", views.appointment_delete, name="appointment_delete"),
]