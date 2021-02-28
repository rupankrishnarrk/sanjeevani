from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class Registration(TemplateView):
    template_name = "registration.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class Profile(TemplateView):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
