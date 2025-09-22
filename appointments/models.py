from django.db import models
from users.models import Doctor, Patient

TIMESLOT_LIST = [
        (0, '08:00 - 08:30'),
        (1, '08:30 - 09:00'),
        (2, '09:00 - 09:30'),
        (3, '10:00 - 10:30'),
        (4, '11:00 - 11:30'),
        (5, '12:00 - 12:30'),
        (6, '13:00 - 13:30'),
        (7, '14:00 - 14:30'),
        (8, '15:00 - 15:30'),
        (9, '16:00 - 16:30'),
        (10, '17:00 - 17:30'),
        (11, '17:00 - 18:00'),
    ]

# Create your models here.
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete = models.CASCADE, blank=True, null=True)
    date = models.DateField()
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('doctor', 'date', 'timeslot')

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date} at {self.timeslot}"
    
