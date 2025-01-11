from hospital_app.forms import (
    HematologyForm,
    LaboratoryRequestFormNurseAndDoctor,
    SerologyForm,
    ClinicalChemistryForm,
    CrossMatchingForm,
    PatientForm,
    CrossMatchingResultForm,
    EmployeeUpdateForm,
    RBSForm,
    UrinalysisForm,
    RBSResultForm,
    LabRequestForm,
)
from hospital_app.models import *
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages


class HematologyUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = HematologyForm
    model = Hematology
    success_url = reverse_lazy("hematology_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully updated hematology information",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update Hematology Details"
        context["humberger_header"] = "Hematology Details"
        return context


class SerologyUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = SerologyForm
    model = Serology
    success_url = reverse_lazy("serology_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request, "You have successfully updated serology information",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update Serology Details"
        context["humberger_header"] = "Serology Details"
        return context


class CrossMatchingResultUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = CrossMatchingResultForm
    model = CrossMatchingResult
    success_url = reverse_lazy("cross_matching_result_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully updated cross-matching result",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update Cross Matching Details"
        context["humberger_header"] = "Cross Matching Details"
        return context


class LabRequestResultUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = LaboratoryRequestFormNurseAndDoctor
    model = LabRequest
    success_url = reverse_lazy("laboratory__result_list")

    def form_valid(self, form):
        lab_request = form.save(commit=False)
        lab_request.requested_by = lab_request.requested_by
        lab_request.save()
        messages.success(
            self.request,
            "You have successfully updated lab request result",
            extra_tags="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update Lab Request Details"
        context["humberger_header"] = "Lab Request Details"
        return context


class RBSResultUpdateView(UpdateView):
    template_name = "forms.html"
    form_class = RBSResultForm
    model = RBSResult
    success_url = reverse_lazy("rbs__result_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully updated RBS result",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "RBS Result Update"
        context["humberger_header"] = "RBS Result Update"
        return context


class CrossMatchingUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = CrossMatchingForm
    model = CrossMatching
    success_url = reverse_lazy("cross_matching_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully updated cross-matching details",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update Cross Matching Details"
        context["humberger_header"] = "Cross Matching Details"
        return context


class PatientUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = PatientForm
    model = Patient
    success_url = reverse_lazy("patient_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully updated patient details",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update Patient Details"
        context["humberger_header"] = "Patient Details"
        return context


class EmployeeUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = EmployeeUpdateForm
    model = CustomUser
    success_url = reverse_lazy("employee_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully updated employee details",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update Employee Details"
        context["humberger_header"] = "Employee Details"
        return context


class ClinicalChemicalUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = ClinicalChemistryForm
    model = ClinicalChemistry
    success_url = reverse_lazy("chemical_chemistry_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully updated clinical chemistry details",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update Clinical Chemistry Detail"
        context["humberger_header"] = "Clinical Chemistry Details"
        return context


class RBSUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = RBSForm
    model = RBS
    success_url = reverse_lazy("rbs_result_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully updated rbs details",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update RBS Details"
        context["humberger_header"] = "RBS Details"
        return context


class UrinalysisUpdateView(UpdateView):
    pk_url_kwarg = "pk"
    template_name = "forms.html"
    form_class = UrinalysisForm
    model = Urinalysis
    success_url = reverse_lazy("urinalysis_result_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully updated urinalysis details",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for form_error in errors:
                messages.error(
                    request=self.request,  
                    message=form_error,    
                    extra_tags="danger"    
                )
        return super().form_invalid(form)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Update Urinalysis Details"
        context["humberger_header"] = "Urinalysis Details"
        return context
