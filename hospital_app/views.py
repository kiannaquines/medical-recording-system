from django.shortcuts import render
from django.views.generic import View, ListView
from hospital_app.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from hospital_app.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

class LoginView(View):
    def get(self, request):
        context = {}
        context['login_form'] = LoginForm()
        return render(request, 'login.html', context)
    
    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('dashboard'))
            
            messages.error(request, 'There was an error while authenticating your account please check your username or password, please try again.')

        return HttpResponseRedirect(reverse_lazy('login'))
    

class DashboardView(View):

    def get(self, request):
        context = {}
        context['detail_header'] = 'Management Dashboard'
        context['humberger_header'] = 'Management Dashboard'

        context['chemical_chemistry_count'] = ClinicalChemistry.objects.all().count()
        context['serology_count'] = Serology.objects.all().count()
        context['hematology_count'] = Hematology.objects.all().count()
        context['cross_matching_count'] = CrossMatching.objects.all().count()


        context['overall_employee'] = User.objects.all().count()
        context['inactive_employee'] = User.objects.filter(is_active=False).count()
        context['active_employee'] = User.objects.filter(is_active=True).count()
        context['employee_group_count'] = Group.objects.all().count()
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
    messages.success(request, 'You have been successfully logged out.')
    return HttpResponseRedirect(reverse_lazy('login'))