from django.shortcuts import get_object_or_404, redirect, render
from hospital_app.forms import (
    EmployeeCreationForm,
    HematologyForm,
    SerologyForm,
    ClinicalChemistryForm,
    CrossMatchingForm,
    PatientForm,
    CrossMatchingResultForm,
    RBSForm,
    UrinalysisForm,
    RBSResultForm,
    LabRequestForm,
    LaboratoryRequestFormNurseAndDoctor,
)
from hospital_app.models import *
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages


class RBSCreateView(CreateView):
    template_name = "forms.html"
    form_class = RBSForm
    model = RBS
    success_url = reverse_lazy("rbs_result_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new rbs.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "RBS Details"
        context["humberger_header"] = "RBS Details"
        return context


class LabRequestCreateView(CreateView):
    template_name = "forms.html"
    form_class = LaboratoryRequestFormNurseAndDoctor
    model = LabRequest
    success_url = reverse_lazy("laboratory__result_list")

    def form_valid(self, form):
        lab_request = form.save(commit=False)
        lab_request.requested_by = self.request.user
        lab_request.save()
        messages.success(
            self.request,
            "You have successfully created a new lab request.",
            extra_tags="primary",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Laboratory Request Details"
        context["humberger_header"] = "Laboratory Request Details"
        return context


class ForAdminLabRequestCreateView(CreateView):
    template_name = "forms.html"
    form_class = LabRequestForm
    model = LabRequest
    success_url = reverse_lazy("laboratory__result_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new lab request.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Laboratory Request Details"
        context["humberger_header"] = "Laboratory Request Details"
        return context


class RBSResultCreateView(CreateView):
    template_name = "forms.html"
    form_class = RBSResultForm
    model = RBSResult
    success_url = reverse_lazy("rbs__result_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new rbs.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "RBS Result Details"
        context["humberger_header"] = "RBS Result Details"
        return context


class UrinalysisCreateView(CreateView):
    template_name = "forms.html"
    form_class = UrinalysisForm
    model = Urinalysis
    success_url = reverse_lazy("urinalysis_result_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new urinalysis result.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Urinalysis Details"
        context["humberger_header"] = "Urinalysis Details"
        return context


class HematologyCreateView(CreateView):
    template_name = "forms.html"
    form_class = HematologyForm
    model = Hematology
    success_url = reverse_lazy("hematology_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new hematology result.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Hematology Details"
        context["humberger_header"] = "Hematology Details"
        return context


class SerologyCreateView(CreateView):
    template_name = "forms.html"
    form_class = SerologyForm
    model = Serology
    success_url = reverse_lazy("serology_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new serology result.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Serology Details"
        context["humberger_header"] = "Serology Details"
        return context


class CrossMatchingResultCreateView(CreateView):
    template_name = "forms.html"
    form_class = CrossMatchingResultForm
    model = CrossMatchingResult
    success_url = reverse_lazy("cross_matching_result_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new cross macthing result.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Cross Matching Details"
        context["humberger_header"] = "Cross Matching Details"
        return context


class CrossMatchingChemicalCreateView(CreateView):
    template_name = "forms.html"
    form_class = CrossMatchingForm
    model = ClinicalChemistry
    success_url = reverse_lazy("cross_matching_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new cross macthing.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Cross Matching Details"
        context["humberger_header"] = "Cross Matching Details"
        return context


class PatientCreateView(CreateView):
    template_name = "forms.html"
    form_class = PatientForm
    model = Patient
    success_url = reverse_lazy("patient_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new patient.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Patient Details"
        context["humberger_header"] = "Patient Details"
        return context


class ClinicalChemicalCreateView(CreateView):
    template_name = "forms.html"
    form_class = ClinicalChemistryForm
    model = ClinicalChemistry
    success_url = reverse_lazy("chemical_chemistry_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new clinical chemistry result.",
            extra_tags="primary",
        )
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request=self.request, messages=error, extra_tags="danger"
                )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Chemical Chemistry Details"
        context["humberger_header"] = "Chemical Chemistry Details"
        return context


class EmployeeCreateView(CreateView):
    template_name = "forms.html"
    form_class = EmployeeCreationForm
    model = CustomUser
    success_url = reverse_lazy("employee_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created a new employee",
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
        context["detail_header"] = "Employee Details"
        context["humberger_header"] = "Employee Details"
        return context
