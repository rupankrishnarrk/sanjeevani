from django import forms
from gui import models
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from gui import validators
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = models.PatientProfileModel
        fields = '__all__'

    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob > datetime.now().date() - timedelta(days=180):
            raise forms.ValidationError('Age must be more than 6 months')
        return dob

    def clean_referral(self):
        if bool(self.cleaned_data['referral']):
            if self.instance.id == self.cleaned_data['referral'].id:
                raise forms.ValidationError('Patient cannot be referral himself ')
        return self.cleaned_data['referral']

    def save(self, createdBy=None, modifiedBy=None):
        record = super(RegistrationForm, self).save(commit=False)
        record.createdBy = createdBy
        record.modifiedBy = modifiedBy
        record.save()
        self.save_m2m()
        return record


class PatientTimelineForm(forms.ModelForm):

    def save(self, pk=None, createdBy=None):
        record = super(PatientTimelineForm, self).save(commit=False)
        record.createdBy = createdBy
        record.patient = pk
        record.save()

    class Meta:
        model = models.PatientTimelineModel
        exclude = ['follow_up_status', 'patient', 'createdBy', 'modifiedBy']


class AppointmentCreateForm(forms.ModelForm):

    starttime = forms.DateTimeField(validators=[validators.validate_datetime_not_in_past])

    def save(self, createdBy=None, modifiedBy=None):
        record = super(AppointmentCreateForm, self).save(commit=False)
        record.createdBy = createdBy
        record.modifiedBy = modifiedBy
        record.save()
        return record

    class Meta:
        model = models.AppointmentModel
        exclude = ['createdBy', 'modifiedBy', 'status']


class AppointmentUpdateForm(forms.ModelForm):

    def clean_starttime(self):
        if self.instance.starttime == self.cleaned_data['starttime']:
            return self.cleaned_data['starttime']
        elif self.cleaned_data['starttime'] <= datetime.now():
                raise ValidationError(
                    _('Entered Datetime should be future datetime or equal to current time')
                )
        else:
            return self.cleaned_data['starttime']

    def save(self, createdBy=None, modifiedBy=None):
        record = super(AppointmentUpdateForm, self).save(commit=False)
        record.createdBy = createdBy
        record.modifiedBy = modifiedBy
        record.save()
        return record

    class Meta:
        model = models.AppointmentModel
        exclude = ['createdBy', 'modifiedBy']


class ReminderForm(forms.ModelForm):

    def save(self, createdBy=None, modifiedBy=None):
        record = super(ReminderForm, self).save(commit=False)
        record.createdBy = createdBy
        record.modifiedBy = modifiedBy
        record.save()
        self.save_m2m()

    class Meta:
        model = models.ReminderModel
        exclude = ['createdBy', 'modifiedBy']

