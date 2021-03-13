from gui import models
from datetime import date
from datetime import datetime
from datetime import timedelta
from django.db.models import Q
import pytz

def dashboard(request):
    today = date.today()
    last_7_days = date.today() - timedelta(days=7)
    after_15_day = date.today() + timedelta(days=15)
    patient = models.PatientProfileModel.objects.filter(createdDate__contains=today)
    appointment = models.AppointmentModel.objects.filter(starttime__contains=today).exclude(visit='Consultation')
    consultation = models.AppointmentModel.objects.filter(starttime__contains=today, visit='Consultation')
    panchakarma_schedule = models.PatientScheduleModel.objects.filter(treatment__type__contains='Therapy', datetime__contains=today)

    appointment_alert =  models.AppointmentModel.objects.filter(starttime__gte=datetime.now() , starttime__lte=datetime.now() + timedelta(days=1)).exclude(visit='Consultation')
    consultation_alert = models.AppointmentModel.objects.filter(starttime__gte=datetime.now(), starttime__lte=datetime.now() + timedelta(days=1), visit='Consultation')
    panchakarma_schedule_alert = models.PatientScheduleModel.objects.filter(treatment__type__contains='Therapy', datetime__gte=datetime.now(), datetime__lte=datetime.now() + timedelta(days=1))
    birthday = models.PatientProfileModel.objects.filter(
        Q(dob__month=last_7_days.month, dob__day__gte=last_7_days.day) | Q(dob__month=after_15_day.month, dob__day__lte=after_15_day.day)
)
    return {
        'profile': patient,
        'appointment': appointment,
        'appointment_alert': appointment_alert,
        'consultation': consultation,
        'consultation_alert': consultation_alert,
        'panchakarma_schedule': panchakarma_schedule,
        'panchakarma_schedule_alert': panchakarma_schedule_alert,
        'birthday': birthday
    }