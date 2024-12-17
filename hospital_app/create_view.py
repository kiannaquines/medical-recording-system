from hospital_app.forms import EmployeeCreationForm, HematologyForm, SerologyForm, ClinicalChemistryForm, CrossMatchingForm, PatientForm, CrossMatchingResultForm
from hospital_app.models import *
from django.views.generic import CreateView
from django.urls import reverse_lazy

class HematologyCreateView(CreateView):
    template_name = 'forms.html'
    form_class = HematologyForm
    model = Hematology
    success_url = reverse_lazy('hematology_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Hematology Details'
        context['humberger_header'] = 'Hematology Details'
        return context
    

class SerologyCreateView(CreateView):
    template_name = 'forms.html'
    form_class = SerologyForm
    model = Serology
    success_url = reverse_lazy('serology_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Serology Details'
        context['humberger_header'] = 'Serology Details'
        return context
    

class CrossMatchingResultCreateView(CreateView):
    template_name = 'forms.html'
    form_class = CrossMatchingResultForm
    model = CrossMatchingResult
    success_url = reverse_lazy('cross_matching_result_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Chemical Chemistry Details'
        context['humberger_header'] = 'Chemical Chemistry Details'
        return context
    

class CrossMatchingChemicalCreateView(CreateView):
    template_name = 'forms.html'
    form_class = CrossMatchingForm
    model = ClinicalChemistry
    success_url = reverse_lazy('cross_matching_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Cross Matching Details'
        context['humberger_header'] = 'Cross Matching Details'
        return context
    

class PatientCreateView(CreateView):
    template_name = 'forms.html'
    form_class = PatientForm
    model = Patient
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Patient Details'
        context['humberger_header'] = 'Patient Details'
        return context
    
class ClinicalChemicalCreateView(CreateView):
    template_name = 'forms.html'
    form_class = ClinicalChemistryForm
    model = ClinicalChemistry
    success_url = reverse_lazy('chemical_chemistry_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Chemical Chemistry Details'
        context['humberger_header'] = 'Chemical Chemistry Details'
        return context
    
class EmployeeCreateView(CreateView):
    template_name = 'forms.html'
    form_class = EmployeeCreationForm
    model = User
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Employee Details'
        context['humberger_header'] = 'Employee Details'
        return context