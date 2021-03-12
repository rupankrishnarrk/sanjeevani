
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
def bmi(value):
    try:
        a = value.height.__str__().split('.')
        h_ft = int(a[0])
        h_inch = int(a[1])
        h_inch += h_ft * 12
        h_cm = round(h_inch * 2.54, 1)
        finalBmi = float(value.weight) / (h_cm / 100 * h_cm / 100)
        if finalBmi < 18.5:
            bmistatus = "Too Thin"
            color = 'warning'
        if finalBmi > 18.5 and finalBmi < 25:
            bmistatus = "Healthy"
            color = 'success'
        if finalBmi > 25:
            bmistatus = "Overweight"
            color = 'danger'
        return {"bmi" : finalBmi, "bmistatus" : bmistatus, "color" : color}
    except:
        return {"bmi": 0, 'bmistatus': 'None', "color" : "danger"}

@register.filter
def lookup(d, key):
    return d[key]
