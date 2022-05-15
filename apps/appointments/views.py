# Create your views here.
import json
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .apis import apis
from .models import Appointment


def clean_data(k, v):
    if k == 'length':
        return timedelta(minutes=float(v))
    if k == 'amount':
        return Decimal(v)
    if k == 'date' or k == 'appointment_made_date':
        return datetime.fromisoformat(v)
    if k == 'time':
        return time.fromisoformat(v)
    return v


def init_kwargs(model, arg_dict):
    model_fields = [f.name for f in model._meta.get_fields()]
    return {k: clean_data(k, v) for k, v in arg_dict.items() if k in model_fields}


@csrf_exempt
@require_http_methods(["POST"])
def AppointmentUpdateWebhookView(request):
    if request.method == 'POST':
        if request.META.get('HTTP_CALLBACK_KEY') != getattr(settings, 'SIKKA_CALLBACK_KEY', ''):
            return HttpResponse('Callback Key Invalid', status=401)

        payload = request.body
        if type(payload) == bytes:
            payload = json.loads(payload)

        # TODO Remove fetch and use payload data:
        if apis.office_id != payload.get('office_id'):
            r = apis.get_authorized_practices(
                office_id=payload.get('office_id'))
        appointments = apis.get_appointments()
        items = appointments.get('items')

        try:
            for appointment in items:
                values = init_kwargs(Appointment, {**appointment})
                Appointment.objects.update_or_create(appointment_sr_no=appointment.get(
                    'appointment_sr_no'), defaults={**values})
        except Exception as e:
            return HttpResponse('Error', status=500)

        return HttpResponse("Webhook received!")
