from django.shortcuts import render
from django.views.generic import View, ListView
from hospital_app.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class LoginView(View):
    def get(self, request):
        context = {}
        return render(request, 'login.html', context)
    
    def post(self, request):
        pass

class DashboardView(View):

    def get(self, request):
        context = {}
        context['detail_header'] = 'Management Dashboard'
        context['humberger_header'] = 'Management Dashboard'
        return render(request, 'dashboard.html', context)

class EmployeeListView(ListView):
    template_name = 'employee.html'
    queryset = User.objects.all()
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Employee Details List'
        context['humberger_header'] = 'Employee Details'
        return context

class PatientListView(ListView):
    template_name = 'patient.html'
    queryset = Patient.objects.all()
    context_object_name = 'patients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Patient Details List'
        context['humberger_header'] = 'Patient Details'
        return context

class ClinicalChemistryView(ListView):
    template_name = 'chemical_chemistry.html'
    queryset = ClinicalChemistry.objects.all()
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Chemical Chemistry Details List'
        context['humberger_header'] = 'Chemical Chemistry Details'
        return context

class HematologyView(ListView):
    template_name = 'hematology.html'
    queryset = Hematology.objects.all()
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Hematology Details List'
        context['humberger_header'] = 'Hematology Details'
        return context

class SerologyView(ListView):
    template_name = 'serology.html'
    queryset = Serology.objects.all()
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Serology Details List'
        context['humberger_header'] = 'Serology Details'
        return context

class CrossMatchingView(ListView):
    template_name = 'cross_matching.html'
    queryset = CrossMatching.objects.all()
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Cross Matching Details List'
        context['humberger_header'] = 'Cross Matching Details'
        return context

class CrossMatchingResultView(ListView):
    template_name = 'cross_matching_result.html'
    queryset = CrossMatchingResult.objects.all()
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Cross Matching Result Details List'
        context['humberger_header'] = 'Cross Matching Result Details'
        return context


def logout_user(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))