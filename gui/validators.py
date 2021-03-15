from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime


def validate_time_in_work_hours(value):
    if value.hour < 6 or value.hour > 8:
        raise ValidationError(
            _('Time is out of working hours')
        )

def validate_datetime_not_in_past(value):
    pass