from django import forms
from gui import models
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User



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


class AppointmentForm(forms.ModelForm):

    def save(self, createdBy=None, modifiedBy=None):
        record = super(AppointmentForm, self).save(commit=False)
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

