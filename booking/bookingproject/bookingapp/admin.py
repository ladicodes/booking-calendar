from django.contrib import admin
from .models import Availability, Appointment
from .forms import AvailabilityForm, AppointmentForm, timedelta


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    form = AvailabilityForm
    list_display = ('title', 'start_time', 'end_time', 'status', 'user')
    list_filter = ('status', 'user')
    date_hierarchy = 'start_time'



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentForm
    list_display = ('name', 'email', 'start_time', 'duration', 'is_confirmed', 'scheduled_with')
    list_filter = ('is_confirmed', 'scheduled_with', 'duration')
    search_fields = ('name', 'email', 'purpose')
    date_hierarchy = 'start_time'
    
    readonly_fields = ('end_time',) 
    
    def save_model(self, request, obj, form, change):
        obj.end_time = obj.start_time + timedelta(minutes=obj.duration)
        super().save_model(request, obj, form, change)