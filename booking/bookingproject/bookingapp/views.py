from django.shortcuts import render
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Availability, Appointment
from django.http import HttpResponse

def generate_schedule_view(request):
    scheduler_user_id = 1 
    

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = today + timedelta(days=7)


    available_blocks = Availability.objects.filter(
        user_id=scheduler_user_id,
        status='A',
        end_time__gt=today,
        start_time__lt=end_date
    ).order_by('start_time')
    
    booked_slots = Appointment.objects.filter(
        scheduled_with_id=scheduler_user_id,
        end_time__gt=today,
        start_time__lt=end_date
    ).order_by('start_time')


    busy_blocks = Availability.objects.filter(
        user_id=scheduler_user_id,
        status='B',
        end_time__gt=today,
        start_time__lt=end_date
    )
    
    taken_slots = list(booked_slots) + list(busy_blocks)

    bookable_slots = []
    slot_duration_minutes = 30 

    for block in available_blocks:
        current_time = block.start_time
        if current_time.minute not in (0, 30):
            current_time = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            if current_time.minute > block.start_time.minute:
                 current_time = current_time.replace(minute=30)
            else:
                current_time = current_time.replace(minute=0)
        

        while current_time + timedelta(minutes=slot_duration_minutes) <= block.end_time:
            slot_start = current_time
            slot_end = current_time + timedelta(minutes=slot_duration_minutes)
            
            is_taken = False
            
            for taken_slot in taken_slots:
                if (taken_slot.start_time < slot_end) and (taken_slot.end_time > slot_start):
                    is_taken = True
                    break
            
            if not is_taken:
                bookable_slots.append({
                    'start': slot_start,
                    'end': slot_end,
                    'duration': slot_duration_minutes,
                    'formatted_time': slot_start.strftime('%I:%M %p')
                })

            current_time = slot_end

    schedule_by_day = {}
    for slot in bookable_slots:
        date_str = slot['start'].date().isoformat() 
        if date_str not in schedule_by_day:
            schedule_by_day[date_str] = []
        schedule_by_day[date_str].append(slot)

    context = {
        'schedule_by_day': schedule_by_day,
        'today': today
    }
    
    return render(request, 'booking/schedule.html', context)