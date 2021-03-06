"""sanjeevani URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gui import views

app_name = "gui"

urlpatterns = [
    path('api/search/patient/', views.PatientSearchView.as_view(), name="patient-search"),
    path('home/', views.Home.as_view(), name="home"),
    path('appointment/', views.AppointmentView.as_view(), name="appointment"),
    path('appointment/<uuid:identifier>/', views.AppointmentUpdateView.as_view(), name="appointment-update"),
    path('patient/profile/<uuid:identifier>/', views.Profile.as_view(), name="profile"),
    path('pagenotfound/', views.PageNotFoundView.as_view(), name="pagenotfound"),
    path('patient/create/', views.PatientProfileCreateView.as_view(), name="patient-create"),
    path('patient/update/<uuid:identifier>/', views.PatientProfileUpdateView.as_view(), name="patient-update"),
]
