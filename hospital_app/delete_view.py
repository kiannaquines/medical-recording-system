from hospital_app.models import *
from django.views.generic import DeleteView
from django.urls import reverse_lazy

class UrinalysisDeleteView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'delete_forms.html'
    model = Urinalysis
    success_url = reverse_lazy('urinalysis_result_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete Urinalysis Details'
        context['humberger_header'] = 'Urinalysis Details'
        return context

class RBSResultDeleteView(DeleteView):
    template_name = 'delete_forms.html'
    model = RBSResult
    success_url = reverse_lazy('rbs__result_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete RBS Result Details'
        context['humberger_header'] = 'Delete RBS Result Details'
        return context 

class RBSDeleteView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'delete_forms.html'
    model = RBS
    success_url = reverse_lazy('rbs_result_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete RBS Details'
        context['humberger_header'] = 'RBS Details'
        return context

class HematologyDeleteView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'delete_forms.html'
    model = Hematology
    success_url = reverse_lazy('hematology_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete Hematology Details'
        context['humberger_header'] = 'Hematology Details'
        return context
    

class SerologyDeleteView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'delete_forms.html'
    model = Serology
    success_url = reverse_lazy('serology_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete Serology Details'
        context['humberger_header'] = 'Serology Details'
        return context
    

class CrossMatchingResultDeleteView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'delete_forms.html'
    model = CrossMatchingResult
    success_url = reverse_lazy('cross_matching_result_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete Chemical Chemistry Details'
        context['humberger_header'] = 'Chemical Chemistry Details'
        return context
    

class CrossMatchingDeleteView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'delete_forms.html'
    model = CrossMatching
    success_url = reverse_lazy('cross_matching_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete Cross Matching Details'
        context['humberger_header'] = 'Cross Matching Details'
        return context
    

class PatientDeleteView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'delete_forms.html'
    model = Patient
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete Patient Details'
        context['humberger_header'] = 'Patient Details'
        return context
    
class ClinicalChemicalDeleteView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'delete_forms.html'
    model = ClinicalChemistry
    success_url = reverse_lazy('chemical_chemistry_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete Chemical Chemistry Detail'
        context['humberger_header'] = 'Chemical Chemistry Details'
        return context
    

class EmployeeDeleteView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'delete_forms.html'
    model = User
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        form = super().form_valid(form)
        return form
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_header'] = 'Delete Employee Details'
        context['humberger_header'] = 'Employee Details'
        return context