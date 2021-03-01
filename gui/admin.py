from django.contrib import admin
from gui import models

# Register your models here.
class PatientProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.PatientProfileModel, PatientProfileAdmin)