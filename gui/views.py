from django.shortcuts import render
from django.views.generic import TemplateView
from gui import  models
from django.views.generic.edit import CreateView, FormView, UpdateView
from gui import forms
from django.shortcuts import  redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import response
from rest_framework import status

allergies_dropdown = ['Drug Allergy', 'Food Allergy', 'Insect Allergy']

# Create your views here.
class Home(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class Profile(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        data = get_object_or_404(models.PatientProfileModel, identifier=kwargs['identifier'])
        form = forms.PatientTimelineForm()
        return render(request, self.template_name, {'patient_data': data, 'form': form, 'active': 'active'})

    def post(self, request, *args, **kwargs):
        data = get_object_or_404(models.PatientProfileModel, identifier=kwargs['identifier'])
        form = forms.PatientTimelineForm(request.POST)
        pk = data
        if form.is_valid():
            form.save(pk=pk)
            return redirect('gui:home')
        print(form.errors)
        return render(request, self.template_name, {'form': form, 'patient_data': data, 'passive': 'active'})


class PageNotFoundView(TemplateView):
    template_name = "404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class PatientProfileCreateView(LoginRequiredMixin, FormView):
    template_name = "patient-create.html"
    form_class = forms.RegistrationForm
    # success_url = reverse_lazy('gui:home')

    def get(self, request, *args, **kwargs):
        profile_base64 = 'data:image/png;base64,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'
        my_referrals = models.PatientProfileModel.objects.all().values('mobile','id')
        return render(request, self.template_name, {'profile_base64': profile_base64,
                                                    'my_referrals': my_referrals,
                                                    'allergies_dropdown': allergies_dropdown
                                                    })

    def post(self, request, *args, **kwargs):
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save(createdBy=request.user)
            return redirect('gui:home')
        print(form.errors)
        return render(request, self.template_name, {'form': form, 'allergies_dropdown': allergies_dropdown })


class PatientProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "patient-update.html"
    form_class = forms.RegistrationForm
    # success_url = reverse_lazy('gui:home')

    def get(self, request, *args, **kwargs):
        data = get_object_or_404(models.PatientProfileModel, identifier=kwargs['identifier'])
        my_referrals = models.PatientProfileModel.objects.all().values('mobile','id')
        return render(request, self.template_name, {'my_referrals': my_referrals, 'data': data,
                                                    'allergies_dropdown': allergies_dropdown
                                                    })

    def post(self, request, *args, **kwargs):
        data = get_object_or_404(models.PatientProfileModel, identifier=kwargs['identifier'])
        form = forms.RegistrationForm(request.POST, instance=data)
        createdBy = data.createdBy
        if form.is_valid():
            form.save(createdBy=createdBy, modifiedBy=request.user)
            return redirect('gui:home')
        print(form.errors)
        return render(request, self.template_name, {'form': form, 'allergies_dropdown': allergies_dropdown })


class PatientSearchView(generics.GenericAPIView):

    def get(self, request):
        if request.is_ajax():
            q = request.GET.get('q', '')
            search = models.PatientProfileModel.objects.filter(mobile__contains=q).values('id', 'mobile')[:5]
            return response.Response(search, status=status.HTTP_200_OK)


class CalendarView(TemplateView):
    template_name = "calendar.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})