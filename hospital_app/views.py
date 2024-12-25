from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView
from hospital_app.models import *
from django.http import (
    FileResponse,
    HttpResponse,
    HttpResponseRedirect,
)
from django.urls import reverse_lazy
from hospital_app.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.settings import BASE_DIR
import io
import os
from fillpdf import fillpdfs


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
    if request.method == "GET":
        try:
            hematology_result = get_object_or_404(Hematology, pk=pk)
            assigned_technologist_details = get_object_or_404(
                EmployeeInfo, user=hematology_result.assigned_technologist
            )
            assigned_pathologistlogist_details = get_object_or_404(
                EmployeeInfo, user=hematology_result.assigned_technologist
            )

            data_to_fill = {
                "name": str(hematology_result.patient),
                "date": hematology_result.get_date(),
                "room": hematology_result.patient.room_number,
                "hemoglobin": f"{str(hematology_result.hemoglobin_mass_concentration)} gm/L",
                "leucocyte": f"{str(hematology_result.leucocyte_no_concentration)} L",
                "hematocrit": str(hematology_result.hematocrit),
                "segmenters": str(hematology_result.segmenters),
                "erythrocyte": f"{str(hematology_result.erythrocty_no_concentration)} L",
                "lymphocytes": str(hematology_result.lymphocytes),
                "platelet": str(hematology_result.platelet),
                "monocytes": str(hematology_result.monocytes),
                "eosinophils": str(hematology_result.eosinophils),
                "bloodtype": str(hematology_result.blood_type),
                "basophils": str(hematology_result.basophils),
                "rhytype": str(hematology_result.rh_type),
                "pathologist_name": str(
                    hematology_result.assigned_pathologist.get_full_name()
                ),
                "medical_technologist_name": str(
                    hematology_result.assigned_technologist.get_full_name()
                ),
                "lic_no_pathologist": str(
                    assigned_pathologistlogist_details.license_number
                ),
                "lic_no_medical_technologist": str(
                    assigned_technologist_details.license_number
                ),
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
    if request.method == "GET":
        try:
            chemical_chemistry_result = get_object_or_404(ClinicalChemistry, pk=pk)
            assigned_technologist_details = get_object_or_404(
                EmployeeInfo, user=chemical_chemistry_result.assigned_technologist
            )
            assigned_pathologistlogist_details = get_object_or_404(
                EmployeeInfo, user=chemical_chemistry_result.assigned_technologist
            )

            data_to_fill = {
                "name": str(chemical_chemistry_result.patient),
                "date": chemical_chemistry_result.get_date(),
                "room": chemical_chemistry_result.patient.room_number,
                "glucose": f"{str(chemical_chemistry_result.glucose)} gm/L",
                "chol": f"{str(chemical_chemistry_result.cholesterol)} L",
                "tri": str(chemical_chemistry_result.triglycerides),
                "hdl": str(chemical_chemistry_result.hdl),
                "ldl": f"{str(chemical_chemistry_result.ldl)} L",
                "cre": str(chemical_chemistry_result.creatinine),
                "uric": str(chemical_chemistry_result.uric_acid),
                "bun": str(chemical_chemistry_result.bun),
                "sgpt": str(chemical_chemistry_result.sgpt),
                "sgot": str(chemical_chemistry_result.sgot),
                "name_path": str(
                    chemical_chemistry_result.assigned_pathologist.get_full_name()
                ),
                "namemedtich": str(
                    chemical_chemistry_result.assigned_technologist.get_full_name()
                ),
                "pat_lic": str(assigned_pathologistlogist_details.license_number),
                "med_tech_lic": str(assigned_technologist_details.license_number),
            }

            input_pdf_path = os.path.join(
                BASE_DIR,
                "hospital_app",
                "templates",
                "pdf_fillables",
                "chemical_chemistry.pdf",
            )

            filled_pdf_buffer = io.BytesIO()
            fillpdfs.write_fillable_pdf(input_pdf_path, filled_pdf_buffer, data_to_fill)
            filled_pdf_buffer.seek(0)

            response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="chemical_chemistry_result_{pk}.pdf"'
            )
            return response

        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def generate_serology_result(request, pk):
    if request.method == "GET":
        try:
            serology_result = get_object_or_404(Serology, pk=pk)
            assigned_technologist_details = get_object_or_404(
                EmployeeInfo, user=serology_result.assigned_technologist
            )
            assigned_pathologistlogist_details = get_object_or_404(
                EmployeeInfo, user=serology_result.assigned_technologist
            )

            data_to_fill = {
                "text_1rlg": str(serology_result.patient),
                "text_2pxsy": serology_result.get_date(),
                "text_3aszy": serology_result.patient.room_number,
                "textarea_4zrvv": f"{str(serology_result.hb_determination)}",
                "textarea_5ugpz": f"{str(serology_result.typhidot_rapid_test)}",
                "textarea_6tjgp": str(serology_result.dengue_rapid_test),
                "text_7cce": str(
                    assigned_pathologistlogist_details.user.get_full_name()
                ),
                "text_8hhqi": f"{str(assigned_technologist_details.user.get_full_name())} L",
                "text_9qfvv": str(assigned_pathologistlogist_details.license_number),
                "text_10wele": str(assigned_technologist_details.license_number),
            }

            input_pdf_path = os.path.join(
                BASE_DIR,
                "hospital_app",
                "templates",
                "pdf_fillables",
                "serology.pdf",
            )

            filled_pdf_buffer = io.BytesIO()
            fillpdfs.write_fillable_pdf(input_pdf_path, filled_pdf_buffer, data_to_fill)
            filled_pdf_buffer.seek(0)

            response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="serology_result_{pk}.pdf"'
            )
            return response

        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def generate_panbio(request, pk):
    if request.method == "GET":
        try:
            patient_info = get_object_or_404(Patient, pk=pk)
            assigned_technologist_details = get_object_or_404(
                EmployeeInfo, user=patient_info.assigned_technologist
            )
            assigned_pathologistlogist_details = get_object_or_404(
                EmployeeInfo, user=patient_info.assigned_technologist
            )

            data_to_fill = {
                "date": str(patient_info.get_date()),
                "lastname": patient_info.lastname,
                "firstname": patient_info.firstname,
                "middlename": f"{str(patient_info.middlename)}",
                "age": f"{str(patient_info.age)}",
                "sex": str(patient_info.sex),
                "physician": str(patient_info.physician.get_full_name()),
                "room": str(patient_info.room_number),
                "sample": str(patient_info.sample_type),
                "time": str(patient_info.get_time_of_collection()),
                "date_collection": str(patient_info.date_of_collection),
                "result": str(patient_info.sars_result),
                "name1": str(assigned_pathologistlogist_details.user.get_full_name()),
                "name2": str(assigned_technologist_details.user.get_full_name()),
                "lic1": str(assigned_pathologistlogist_details.license_number),
                "lic2": str(assigned_technologist_details.license_number),
            }

            input_pdf_path = os.path.join(
                BASE_DIR,
                "hospital_app",
                "templates",
                "pdf_fillables",
                "panbio_template.pdf",
            )

            filled_pdf_buffer = io.BytesIO()
            fillpdfs.write_fillable_pdf(input_pdf_path, filled_pdf_buffer, data_to_fill)
            filled_pdf_buffer.seek(0)

            response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="panbio_{pk}.pdf"'
            return response

        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def generate_cross_matching_result(request, id):
    pass
