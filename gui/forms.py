from django import forms
from gui import models
from datetime import datetime
from datetime import timedelta


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = models.PatientProfileModel
        fields = '__all__'

    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob > datetime.now().date() - timedelta(days=180):
            raise forms.ValidationError('Age must be more than 6 months')
        return dob

    def save(self, createdBy=None):
        record = super(RegistrationForm, self).save(commit=False)
        if createdBy:
            record.createdBy = createdBy
        record.save()