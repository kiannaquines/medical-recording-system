from PyPDF2 import PdfReader, PdfWriter
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView
from hospital_app.models import *
from django.http import (
    FileResponse,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.urls import reverse_lazy
from hospital_app.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.settings import BASE_DIR
import io
import os
from fillpdf import fillpdfs
import tempfile


class LoginView(View):
    def get(self, request):
        context = {}
        context["login_form"] = LoginForm()
        return render(request, "login.html", context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy("dashboard"))

            messages.error(
                request,
                "There was an error while authenticating your account please check your username or password, please try again.",
            )

        return HttpResponseRedirect(reverse_lazy("login"))


class DashboardView(View):

    def get(self, request):
        context = {}
        context["detail_header"] = "Management Dashboard"
        context["humberger_header"] = "Management Dashboard"

        context["chemical_chemistry_count"] = ClinicalChemistry.objects.all().count()
        context["serology_count"] = Serology.objects.all().count()
        context["hematology_count"] = Hematology.objects.all().count()
        context["cross_matching_count"] = CrossMatching.objects.all().count()

        context["overall_employee"] = User.objects.all().count()
        context["inactive_employee"] = User.objects.filter(is_active=False).count()
        context["active_employee"] = User.objects.filter(is_active=True).count()
        context["employee_group_count"] = Group.objects.all().count()
        return render(request, "dashboard.html", context)


class EmployeeListView(ListView):
    template_name = "employee.html"
    queryset = User.objects.all()
    context_object_name = "employees"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Employee Details List"
        context["humberger_header"] = "Employee Details"
        return context


class PatientListView(ListView):
    template_name = "patient.html"
    queryset = Patient.objects.all()
    context_object_name = "patients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Patient Details List"
        context["humberger_header"] = "Patient Details"
        return context


class ClinicalChemistryView(ListView):
    template_name = "chemical_chemistry.html"
    queryset = ClinicalChemistry.objects.all()
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Chemical Chemistry Details List"
        context["humberger_header"] = "Chemical Chemistry Details"
        return context


class HematologyView(ListView):
    template_name = "hematology.html"
    queryset = Hematology.objects.all()
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Hematology Details List"
        context["humberger_header"] = "Hematology Details"
        return context


class SerologyView(ListView):
    template_name = "serology.html"
    queryset = Serology.objects.all()
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Serology Details List"
        context["humberger_header"] = "Serology Details"
        return context


class CrossMatchingView(ListView):
    template_name = "cross_matching.html"
    queryset = CrossMatching.objects.all()
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Cross Matching Details List"
        context["humberger_header"] = "Cross Matching Details"
        return context


class CrossMatchingResultView(ListView):
    template_name = "cross_matching_result.html"
    queryset = CrossMatchingResult.objects.all()
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Cross Matching Result Details List"
        context["humberger_header"] = "Cross Matching Result Details"
        return context


def logout_user(request):
    from django.contrib.auth import logout

    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return HttpResponseRedirect(reverse_lazy("login"))


def generate_hematology_result(request, pk):
    try:
        hematology_result = get_object_or_404(Hematology, pk=pk)

        data_to_fill = {
            "name": str(hematology_result.patient),
            "date": hematology_result.get_date(),
            "room": hematology_result.patient.room_number,
            "hemoglobin": str(hematology_result.hemoglobin_mass_concentration or ""),
            "leucocyte": str(hematology_result.leucocyte_no_concentration or ""),
            "hematocrit": str(hematology_result.hematocrit or ""),
            "segmenters": str(hematology_result.segmenters or ""),
            "erythrocyte": str(hematology_result.erythrocty_no_concentration or ""),
            "lymphocytes": str(hematology_result.lymphocytes or ""),
            "platelet": str(hematology_result.platelet or ""),
            "monocytes": str(hematology_result.monocytes or ""),
            "eosinophils": str(hematology_result.eosinophils or ""),
            "bloodtype": str(hematology_result.blood_type or ""),
            "basophils": str(hematology_result.basophils or ""),
            "rhytype": str(hematology_result.rh_type or ""),
        }

        input_pdf_path = os.path.join(
            BASE_DIR,
            "hospital_app",
            "templates",
            "pdf_fillables",
            "hematology_form_fillable.pdf",
        )

        filled_pdf_buffer = io.BytesIO()
        fillpdfs.write_fillable_pdf(input_pdf_path, filled_pdf_buffer, data_to_fill)
        filled_pdf_buffer.seek(0)

        response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="hematology_result_{pk}.pdf"'
        )
        return response

    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def generate_chemistry_result(request, pk):
    pass


def generate_serology_result(request, id):
    pass


def generate_cross_matching_result(request, id):
    pass
