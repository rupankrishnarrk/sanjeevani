from django.contrib import admin
from gui import models
from django.contrib.admin.utils import flatten_fieldsets


# Register your models here.
class PatientProfileAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.PatientProfileModel, PatientProfileAdmin)