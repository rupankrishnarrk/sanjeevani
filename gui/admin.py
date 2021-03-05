from django.contrib import admin
from gui import models
from datetime import datetime
import nested_admin


# Register your models here.
# @admin.register(models.PatientProfileModel)
# class PatientProfileAdmin(admin.ModelAdmin):
#     list_display = ['identifier', 'get_full_name', 'mobile', 'gender', 'createdDate',
#                     'modifiedDate', 'createdBy', 'modifiedBy']
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False


@admin.register(models.StaffProfileModel)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['designation', 'name', 'mobile', 'createdDate', 'modifiedDate']
    readonly_fields = ['createdBy', 'modifiedBy']

    def save_model(self, request, rows, form, change):
        if rows._state.adding:
            rows.createdBy_id = request.user.id
        else:
            rows.modifiedDate = datetime.now()
            rows.modifiedBy_id = request.user.id
        super().save_model(request, rows, form, change)


class PatientScheduleAdmin(nested_admin.NestedTabularInline):
    model = models.PatientScheduleModel
    ordering = ('datetime',)
    extra = 0


class PatientFileAdmin(nested_admin.NestedTabularInline):
    model = models.PatientFilesModel
    ordering = ('file',)
    extra = 0


class PatientTimelineAdmin(nested_admin.NestedTabularInline):
    model = models.PatientTimelineModel
    extra = 0


@admin.register(models.AllergiesModel)
class AllergiesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PatientProfileModel)
class PatientProfileAdmin(nested_admin.NestedModelAdmin):
    inlines = [PatientTimelineAdmin]
    list_display = ['identifier', 'get_full_name', 'mobile', 'gender', 'createdDate',
                    'modifiedDate', 'createdBy', 'modifiedBy']

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False