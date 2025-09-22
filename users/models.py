from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
        ('admin', 'Admin')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)



# Doctors model
class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    profile_picture = models.ImageField(upload_to='profile_pic/doctor_profiles/', null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ahpra = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    departhment = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def get_id(self):
         return self.user.id
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# Patients model
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='patient_profiles/', null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    medicare_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    status = models.BooleanField(default=True)

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def get_id(self):
         return self.user.id
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

# Staff model
class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='staff_profiles/', null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    position = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def get_id(self):
         return self.user.id
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

