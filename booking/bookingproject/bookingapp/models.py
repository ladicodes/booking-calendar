from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Availability(models.Model):

    AVAILABILITY_CHOICES = [
        ('A', 'Available'),
        ('B', 'Busy/Blocked'),
    ]

    title = models.CharField(max_length=200, help_text="e.g., 'Weekly Working Hours' or 'Vacation Block'")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES, default='A',
                              help_text="A = Available (Default), B = Busy (Blocks scheduling)")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) # Links to your user account

    class Meta:
        verbose_name_plural = "Availability Blocks (Your Schedule)"
    def __str__(self):
        return f"{self.title} ({self.status}) from {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Appointment(models.Model):
  
    MEETING_LENGTH_CHOICES = [
        (30, '30 Minutes'),
        (60, '60 Minutes'),
    ]

   
    name = models.CharField(max_length=100)
    email = models.EmailField()
    purpose = models.TextField(help_text="What is the meeting about?")
    
    # Scheduling fields
    start_time = models.DateTimeField(unique=True) 
    end_time = models.DateTimeField()            
    duration = models.IntegerField(choices=MEETING_LENGTH_CHOICES, default=30)
    
    # Internal status
    is_confirmed = models.BooleanField(default=False)
    scheduled_with = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 

    class Meta:
        verbose_name_plural = "Booked Appointments"
        ordering = ['start_time']

    def __str__(self):
        return f"Call with {self.name} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"