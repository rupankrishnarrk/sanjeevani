
from django import template
from gui import models
import random


register = template.Library()

@register.filter
def referral_tag(value):
    try:
        return models.PatientProfileModel.objects.get(id=value).mobile
    except:
        return ""

@register.filter
def random_allergies_label(value):
    labels = ['primary', 'info', 'danger', 'success', 'warning']
    return random.choice(labels)
