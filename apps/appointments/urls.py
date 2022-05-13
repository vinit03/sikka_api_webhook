from django.urls import path

from .views import AppointmentUpdateWebhookView

app_name = 'appointments'

urlpatterns = [
    path('appointments/payload', AppointmentUpdateWebhookView, name='weebhook')
]
