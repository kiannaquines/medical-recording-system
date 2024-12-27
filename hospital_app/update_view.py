from hospital_app.forms import HematologyForm, SerologyForm, ClinicalChemistryForm, CrossMatchingForm, PatientForm, CrossMatchingResultForm, EmployeeUpdateForm, RBSForm, UrinalysisForm
from hospital_app.models import *
from django.views.generic import UpdateView
from django.urls import reverse_lazy

class HematologyUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
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
        context['detail_header'] = 'Update Hematology Details'
        context['humberger_header'] = 'Hematology Details'
        return context
    
class SerologyUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
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
        context['detail_header'] = 'Update Serology Details'
        context['humberger_header'] = 'Serology Details'
        return context
    
class CrossMatchingResultUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
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
        context['detail_header'] = 'Update Cross Matching Details'
        context['humberger_header'] = 'Cross Matching Details'
        return context
    
class CrossMatchingUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
    template_name = 'forms.html'
    form_class = CrossMatchingForm
    model = CrossMatching
    success_url = reverse_lazy('cross_matching_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Update Cross Matching Details'
        context['humberger_header'] = 'Cross Matching Details'
        return context
    
class PatientUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
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
        context['detail_header'] = 'Update Patient Details'
        context['humberger_header'] = 'Patient Details'
        return context

class EmployeeUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
    template_name = 'forms.html'
    form_class = EmployeeUpdateForm
    model = User
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Update Employee Details'
        context['humberger_header'] = 'Employee Details'
        return context
    
class ClinicalChemicalUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
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
        context['detail_header'] = 'Update Chemical Chemistry Detail'
        context['humberger_header'] = 'Chemical Chemistry Details'
        return context
    

class RBSUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
    template_name = 'forms.html'
    form_class = RBSForm
    model = RBS
    success_url = reverse_lazy('rbs_result_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Update RBS Details'
        context['humberger_header'] = 'RBS Details'
        return context
    

class UrinalysisUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
    template_name = 'forms.html'
    form_class = UrinalysisForm
    model = Urinalysis
    success_url = reverse_lazy('urinalysis_result_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Update Urinalysis Details'
        context['humberger_header'] = 'Urinalysis Details'
        return context