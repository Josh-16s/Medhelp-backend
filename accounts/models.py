from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    )

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    adress = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    

    age = models.IntegerField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    default_latitude = models.FloatField(null=True, blank=True)
    default_longitude = models.FloatField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

