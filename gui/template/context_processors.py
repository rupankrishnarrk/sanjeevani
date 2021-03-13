from gui import models
from datetime import date
from datetime import datetime
import pytz

def dashboard(request):
    today = date.today()
    patient = models.PatientProfileModel.objects.filter(createdDate__contains=today)
    appointment = models.AppointmentModel.objects.filter(starttime__contains=today).exclude(visit='Consultation')
    consultation = models.AppointmentModel.objects.filter(starttime__contains=today, visit='Consultation')
    panchakarma_schedule = models.PatientScheduleModel.objects.filter(treatment__type__contains='Therapy', datetime__contains=today)
    return {
        'profile': patient,
        'appointment': appointment,
        'consultation': consultation,
        'panchakarma_schedule': panchakarma_schedule
    }

