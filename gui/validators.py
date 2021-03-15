from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime


def validate_datetime_not_in_past(value):
    print(value)
    print(datetime.now())
    print(type(value))
    if value <= datetime.now():
        raise ValidationError(
            _('Entered Datetime should be future datetime or equal to current time')
        )