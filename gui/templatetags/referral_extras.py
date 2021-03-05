
from django import template
from gui import models


register = template.Library()

@register.filter
def referral_tag(value):
    print(value)
    try:
        return models.PatientProfileModel.objects.get(id=value).mobile
    except:
        return ""