from django import forms
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Availability, Appointment

class BaseScheduleForm(forms.ModelForm):
 
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError("The end time must be after the start time.")
            
            instance_pk = self.instance.pk if self.instance else None

            conflicting_appointments = Appointment.objects.filter(
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=instance_pk)

            if conflicting_appointments.exists():
                raise ValidationError("This time slot conflicts with an existing Appointment.")
            
            conflicting_availability = Availability.objects.filter(
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=instance_pk)

            if conflicting_availability.exists():

                busy_blocks = conflicting_availability.filter(status='B')
                if busy_blocks.exists():
                    raise ValidationError("This time slot conflicts with a 'Busy' block in your schedule.")
                
        return cleaned_data

class AvailabilityForm(BaseScheduleForm):
    class Meta:
        model = Availability
        fields = '__all__'


class AppointmentForm(BaseScheduleForm):
    class Meta:
        model = Appointment
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        duration = cleaned_data.get('duration')

        if start_time and end_time and duration:
            expected_end = start_time + timedelta(minutes=duration)
            
            if end_time != expected_end:
                raise ValidationError(f"End time must be exactly {duration} minutes after the start time.")
        if start_time and end_time:
            is_available = Availability.objects.filter(
                start_time__lte=start_time,
                end_time__gte=end_time,
                status='A'
            ).exists()

            if not is_available:
                raise ValidationError("This appointment time is outside of a defined 'Available' block.")
        
        return cleaned_data