from django.urls import path
from . import views

app_name = 'bookingapp'

urlpatterns = [
    path('', views.generate_schedule_view, name='schedule_home'),
    path('book/', views.book_appointment, name='book_appointment'),
]