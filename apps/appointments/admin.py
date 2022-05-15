from atexit import register

from django.contrib import admin

from .models import Appointment

# Register your models here.


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_sr_no', 'patient_name', 'date',)
    search_fields = ('patient_name', 'patient_id')
    ordering = ('date',)
