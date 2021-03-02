
from django import template
from gui import models


register = template.Library()

@register.filter
def referral_tag(value):
    return models.PatientProfileModel.objects.get(id=value).mobile