from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Appointment(models.Model):
    href = models.URLField(_('Appointment URL'))
    patient_id = models.CharField(_('Patient ID'), max_length=10)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=4)
    note = models.TextField(_('Note'), max_length=5000)
    appointment_sr_no = models.CharField(
        _('Appointment ID'), unique=True, db_index=True, max_length=25)
    date = models.DateTimeField(_('Date'))
    time = models.TimeField(_('Time'))
    length = models.DurationField(_('Duration'))
    description = models.TextField(_('Description'), max_length=5000)
    appointment_made_date = models.DateTimeField('Appoinment Made On')
    type = models.CharField(_('Type'), max_length=50)
    patient_name = models.CharField(_('Patients Name'), max_length=100)
    patient_href = models.URLField(_('Patients URL'))

    # 			"patient_href": "https://api.sikkasoft.com/v4/practices/1/patients/159801",
    # 			"guarantor_id": "",
    # 			"provider_id": "20",
    # 			"provider_href": "https://api.sikkasoft.com/v4/practices/1/providers/20",
    # 			"practice_id": "1",
    # 			"practice_href": "https://api.sikkasoft.com/v4/practices/1",
    # 			"guarantor_href": "https://api.sikkasoft.com/v4/practices/1/guarantors/",
    # 			"surface_quadrant_type": "",
    # 			"appointment_made_date": "2021-05-26T00:00:00",
    # 			"type": "General",
    # 			"procedure_code1": "1110",
    # 			"procedure_code1_amount": "115.0000",
    # 			"procedure_code2": "1204",
    # 			"procedure_code2_amount": "52.0000",
    # 			"procedure_code3": "0",
    # 			"procedure_code3_amount": "0.0000",
    # 			"guarantor_name": "",
    # 			"procedure_code1_time": "30.00000",
    # 			"procedure_code2_time": "0.00000",
    # 			"procedure_code3_time": "0.00000",
    # 			"surface_quadrant": "",
    # 			"cust_id": "1",
    # 			"rowhash": ""
