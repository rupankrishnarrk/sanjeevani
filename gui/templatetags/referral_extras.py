
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

@register.filter
def file_label(value):
    labels = {
        "Radiology Report": { "icon" : "fa-heartbeat", "color" : "MediumSeaGreen"},
        "Laboratory Report": { "icon" : "fa-flask", "color" : "#ff8c00"},
        "Medical Prescription": { "icon": "fa-medkit", "color" : "#ce5642"},
        "Medical Report": { "icon": "fa-file-text", "color" : "SlateBlue"}
    }
    return labels[value]

@register.filter
def lookup(d, key):
    return d[key]