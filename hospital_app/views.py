from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView
from hospital_app.models import *
from django.http import (
    FileResponse,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.urls import reverse_lazy
from hospital_app.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.settings import BASE_DIR
import io
import os
from fillpdf import fillpdfs
from django.contrib.admin.models import LogEntry
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from core.settings import LOGO_PATH
from reportlab.lib.pagesizes import letter
from django.utils.text import slugify
from datetime import datetime
import json


def view_patient_informations(request):

    from django.db.models import Prefetch

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    patient_id = body.get("patient_id")
    room_number = body.get("room_number")
    age = body.get("age")

    if not all([patient_id, room_number, age]):
        return JsonResponse({"error": "Missing required fields: patient_id, room_number, or age."}, status=400)

    try:
        patient = Patient.objects.get(pk=patient_id, room_number=room_number, age=age)
    except Patient.DoesNotExist:
        return JsonResponse({"success": False, "error": "Patient not found with the provided information."}, status=404)

    patient_info = {
        'fullname': patient.get_full_name(),
        'age': patient.age,
        'gender': patient.sex,
        'patient_type': patient.patient_type,
        'physician': patient.physician.get_full_name() if patient.physician else None,
        'room_number': patient.room_number,
        'sample_type': patient.sample_type,
        'sars_result': patient.sars_result,
        'date': patient.date.isoformat() if patient.date else None,
    }

    cross_matching_data = CrossMatching.objects.filter(patient__id=patient_id).prefetch_related(
        Prefetch(
            'results',
            queryset=CrossMatchingResult.objects.all(),
        )
    )

    rbs_data = RBS.objects.filter(patient__id=patient_id).prefetch_related(
        Prefetch(
            'rbs_result',
            queryset=RBSResult.objects.all(),
        )
    )


    output_cross_matching = []
    for cross_matching in cross_matching_data:
        output_cross_matching.append({
            "id": cross_matching.id,
            "patient": str(cross_matching.patient),
            "pathologist": str(cross_matching.pathologist),
            "medical_technologist": str(cross_matching.medical_technologist),
            "created_at": cross_matching.created_at,
            "updated_at": cross_matching.updated_at,
            "results": [
                {
                    "serial_no": result.serial_no,
                    "amt_in_cc": result.amt_in_cc,
                    "blood_bank": result.blood_bank,
                    "date_of_collection": result.date_of_collection,
                    "expiration_date": result.expiration_date,
                    "result": result.result,
                }
                for result in cross_matching.results.all()
            ],
        })
    
    output_rbs_result = []
    for rbs in rbs_data:
        output_rbs_result.append({
            "id": rbs.id,
            "patient": str(rbs.patient),
            "pathologist": str(rbs.assigned_pathologist) if rbs.assigned_pathologist else None,
            "medical_technologist": str(rbs.assigned_technologist) if rbs.assigned_technologist else None,
            "results": [
                {
                    "result": result.result,
                    "date": result.date.strftime("%m/%d/%Y"),
                    "time": result.time.strftime("%I:%M %p"),
                }
                for result in rbs.rbs_result.all()
            ],
        })




    related_data = {
        "clinical_chemistry": list(ClinicalChemistry.objects.filter(patient__id=patient_id).values('glucose','cholesterol','triglycerides','hdl','ldl','creatinine', 'uric_acid', 'bun', 'sgpt', 'sgot', 'date')),
        "serology": list(Serology.objects.filter(patient__id=patient_id).values('hb_determination','typhidot_rapid_test','dengue_rapid_test','date')),
        "hematology": list(Hematology.objects.filter(patient__id=patient_id).values('hemoglobin_mass_concentration','hematocrit','erythrocty_no_concentration','platelet','blood_type','rh_type','leucocyte_no_concentration','segmenters','lymphocytes','monocytes','eosinophils','basophils','date')),
        "cross_matching": output_cross_matching,
        "urinalysis": Urinalysis.objects.filter(patient__id=patient_id).values('color','appearance','specific_gravity','pH','sugar','albumin','epithelia','bacteria','pus_cells','rbc','cast','crystals','others','amorphous','mucous_thread','pregnancy_test','urates').first(),
        "rbs": output_rbs_result,
    }

    return JsonResponse(
        {
            "success": True,
            "patient_info": patient_info,
            **related_data,
        }
    )


def generate_report(request):
    if request.method == "GET":
        patient_type = request.GET.get("patient_type")
        start_date = (
            datetime.strptime(request.GET.get("start_date"), "%Y-%m-%d").date()
            if request.GET.get("start_date")
            else None
        )
        end_date = (
            datetime.strptime(request.GET.get("end_date"), "%Y-%m-%d").date()
            if request.GET.get("end_date")
            else None
        )

        clinical_chemistry = ClinicalChemistry.objects.filter(
            patient__patient_type=patient_type
        )
        serology = Serology.objects.filter(
            patient__patient_type=patient_type,
        )
        hematology = Hematology.objects.filter(patient__patient_type=patient_type)
        cross_matching = CrossMatching.objects.filter(
            patient__patient_type=patient_type
        )
        urinalysis = Urinalysis.objects.filter(patient__patient_type=patient_type)

        if start_date and end_date:
            clinical_chemistry = clinical_chemistry.filter(
                date__range=[start_date, end_date]
            ).count()
            serology = serology.filter(date__range=[start_date, end_date]).count()
            hematology = hematology.filter(date__range=[start_date, end_date]).count()
            cross_matching = cross_matching.filter(
                created_at__range=[start_date, end_date]
            ).count()
            urinalysis = urinalysis.filter(
                created_at__range=[start_date, end_date]
            ).count()
        else:
            clinical_chemistry = clinical_chemistry.count()
            serology = serology.count()
            hematology = hematology.count()
            cross_matching = cross_matching.count()
            urinalysis = urinalysis.count()

        data = {
            "clinical_chemistry": {
                "total": clinical_chemistry,
                "name": f"Clinical Chemistry Request {patient_type}",
            },
            "serology": {
                "total": serology,
                "name": f"Serology {patient_type}",
            },
            "hematology": {
                "total": hematology,
                "name": f"Hematology {patient_type}",
            },
            "cross_matching": {
                "total": cross_matching,
                "name": f"Cross Matching {patient_type}",
            },
            "urinalysis": {
                "total": urinalysis,
                "name": f"Urinalysis Request {patient_type}",
            },
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "header_report_type": (
                f"Report from {start_date} to {end_date}"
                if start_date and end_date
                else "Overall Report"
            ),
        }

        return JsonResponse(data)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


class LoginView(View):
    def get(self, request):
        context = {}
        context["login_form"] = LoginForm()
        context["patients"] = Patient.objects.all().order_by("-date")
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
                extra_tags="danger",
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

        context["overall_employee"] = CustomUser.objects.all().count()
        context["inactive_employee"] = CustomUser.objects.filter(is_active=False).count()
        context["active_employee"] = CustomUser.objects.filter(is_active=True).count()
        context["employee_group_count"] = Group.objects.all().count()
        context["logs"] = LogEntry.objects.select_related(
            "user", "content_type"
        ).order_by("-action_time")
        return render(request, "dashboard.html", context)


class EmployeeListView(ListView):
    template_name = "employee.html"
    queryset = CustomUser.objects.all().order_by("-date_joined")
    context_object_name = "employees"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Employee Details List"
        context["humberger_header"] = "Employee Details"
        return context


class LaboratoryRequestView(ListView):
    template_name = "lab_request.html"
    queryset = LabRequest.objects.all().order_by("-date_request")
    context_object_name = "results"

    def get_queryset(self):
        current_user = self.request.user
        if (
            current_user.groups.filter(Q(name="Medical Technologist")).exists()
            or current_user.groups.filter(Q(name="Administrator")).exists()
        ):
            return LabRequest.objects.all().order_by("-date_request")
        return LabRequest.objects.filter(requested_by=current_user).order_by(
            "-date_request"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["detail_header"] = "Laboratory Request List"
        context["humberger_header"] = "Laboratory Request"
        context["hematology_count"] = LabRequest.objects.filter(
            lab_request_type="Hematology"
        ).count()
        context["serology_count"] = LabRequest.objects.filter(
            lab_request_type="Serology"
        ).count()
        context["clinical_chemistry_count"] = LabRequest.objects.filter(
            lab_request_type="Clinical Chemistry"
        ).count()
        context["cross_matching_count"] = LabRequest.objects.filter(
            lab_request_type="Cross Matching"
        ).count()
        context["urinalysis_count"] = LabRequest.objects.filter(
            lab_request_type="Urinalysis"
        ).count()
        context["rbs_count"] = LabRequest.objects.filter(lab_request_type="RBS").count()
        context["overall_results"] = LabRequest.objects.count()

        return context


class PatientListView(ListView):
    template_name = "patient.html"
    queryset = Patient.objects.all().order_by("-date")
    context_object_name = "patients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Patient Details List"
        context["humberger_header"] = "Patient Details"
        return context


class PatientPanBioListView(ListView):
    template_name = "patient_bio.html"
    queryset = Patient.objects.all().order_by("-date")
    context_object_name = "patients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Patient Bio"
        context["humberger_header"] = "Patient Bio"
        return context


class ClinicalChemistryView(ListView):
    template_name = "chemical_chemistry.html"
    queryset = ClinicalChemistry.objects.all().order_by("-date")
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Clinical Chemistry Details List"
        context["humberger_header"] = "Clinical Chemistry Details"
        return context


class RBSView(ListView):
    template_name = "rbs.html"
    queryset = RBS.objects.all()
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "RBS Details List"
        context["humberger_header"] = "RBS Details"
        return context


class PatientRBSView(ListView):
    template_name = "rbs_results.html"
    queryset = RBSResult.objects.all()
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "RBS Result Details List"
        context["humberger_header"] = "RBS Result Details"
        return context


class UrinalysisView(ListView):
    template_name = "urinalysis.html"
    queryset = Urinalysis.objects.all()
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "Urinalysis Details List"
        context["humberger_header"] = "Urinalysis Details"
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
                    '123445'
                ),
                "lic_no_medical_technologist": str(
                    '233442'
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

            filename = f"hematology_result_{slugify(hematology_result.patient.get_full_name())}_{datetime.now().strftime('%Y%m%d')}.pdf"

            response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def generate_chemistry_result(request, pk):
    if request.method == "GET":
        try:
            chemical_chemistry_result = get_object_or_404(ClinicalChemistry, pk=pk)
            
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
                "pat_lic": str('123234'),
                "med_tech_lic": str('123234'),
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
            filename = f"chemistry_result_{slugify(chemical_chemistry_result.patient.get_full_name())}_{datetime.now().strftime('%Y%m%d')}.pdf"
            response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def generate_serology_result(request, pk):
    if request.method == "GET":
        try:
            serology_result = get_object_or_404(Serology, pk=pk)
            

            data_to_fill = {
                "text_1rlg": str(serology_result.patient),
                "text_2pxsy": serology_result.get_date(),
                "text_3aszy": serology_result.patient.room_number,
                "textarea_4zrvv": f"{str(serology_result.hb_determination)}",
                "textarea_5ugpz": f"{str(serology_result.typhidot_rapid_test)}",
                "textarea_6tjgp": str(serology_result.dengue_rapid_test),
                "text_7cce": str(
                    serology_result.user.get_full_name()
                ),
                "text_8hhqi": f"{str(serology_result.user.get_full_name())} L",
                "text_9qfvv": str(serology_result.license_number),
                "text_10wele": str(serology_result.license_number),
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
            filename = f"serology_result_{slugify(serology_result.patient.get_full_name())}_{datetime.now().strftime('%Y%m%d')}.pdf"
            response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="={filename}"'
            return response

        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def generate_panbio(request, pk):
    if request.method == "GET":
        try:
            patient_info = get_object_or_404(Patient, pk=pk)
            

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
                "name1": str(patient_info.user.get_full_name()),
                "name2": str(patient_info.user.get_full_name()),
                "lic1": str(patient_info.license_number),
                "lic2": str(patient_info.license_number),
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
            filename = f"panbio_result_{slugify(patient_info.get_full_name())}_{datetime.now().strftime('%Y%m%d')}.pdf"
            response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def generate_urinalysis_result(request, pk):
    if request.method == "GET":
        try:
            urinalysis_detail = get_object_or_404(Urinalysis, pk=pk)
            

            data_to_fill = {
                "name": str(urinalysis_detail.patient),
                "date": urinalysis_detail.get_date(),
                "room": urinalysis_detail.patient.room_number,
                "color": urinalysis_detail.color,
                "appearance": urinalysis_detail.appearance,
                "reaction": urinalysis_detail.pH,
                "gravity": urinalysis_detail.specific_gravity,
                "sugar": urinalysis_detail.sugar,
                "albumin": urinalysis_detail.albumin,
                "cells": urinalysis_detail.epithelia,
                "pus": urinalysis_detail.pus_cells,
                "rbs": urinalysis_detail.rbc,
                "mucous": urinalysis_detail.mucous_thread,
                "cast": urinalysis_detail.cast,
                "crystals": urinalysis_detail.crystals,
                "urates": urinalysis_detail.urates,
                "bacteria": urinalysis_detail.bacteria,
                "others": urinalysis_detail.others,
                "pregnancy_test": urinalysis_detail.pregnancy_test,
                "name1": urinalysis_detail.user.get_full_name(),
                "name2": urinalysis_detail.user.get_full_name(),
                "lic1": urinalysis_detail.license_number,
                "lic2": urinalysis_detail.license_number,
            }

            input_pdf_path = os.path.join(
                BASE_DIR,
                "hospital_app",
                "templates",
                "pdf_fillables",
                "urinalysis_template.pdf",
            )

            filled_pdf_buffer = io.BytesIO()
            fillpdfs.write_fillable_pdf(input_pdf_path, filled_pdf_buffer, data_to_fill)
            filled_pdf_buffer.seek(0)
            filename = f"urinalysis_result_{slugify(urinalysis_detail.patient)}_{datetime.now().strftime('%Y%m%d')}.pdf"
            response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def add_logo(canvas, doc):
    canvas.drawImage(
        LOGO_PATH,
        x=doc.leftMargin - 0.7 * inch,
        y=doc.pagesize[1] - 1.5 * inch,
        width=1.2 * inch,
        height=1.2 * inch,
        preserveAspectRatio=True,
        mask="auto",
    )


def generate_cross_matching_result(request, pk):
    if request.method == "GET":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=0.5 * inch,
            leftMargin=1 * inch,
            rightMargin=1 * inch,
            bottomMargin=1 * inch,
        )

        elements = []
        styles = getSampleStyleSheet()
        styles["Normal"].fontSize = 11

        header_style = ParagraphStyle(
            "CustomHeader",
            parent=styles["Normal"],
            fontSize=12,
            alignment=1,
            spaceAfter=0,
            spaceBefore=0,
            leading=15,
            textColor=colors.black,
        )

        header_content = [
            [
                Paragraph(
                    "<b>PRESIDENT ROXAS PROVINCIAL COMMUNITY HOSPITAL</b><br/>"
                    "New Cebu, Pres. Roxas, Cotabato.<br/>"
                    "<b>LABORATORY DEPARTMENT</b><br/>"
                    "<b>CROSS MATCHING RESULT</b>",
                    header_style,
                ),
            ]
        ]

        header_table = Table(header_content, colWidths=[7.3 * inch])
        header_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        elements.append(header_table)
        elements.append(Spacer(1, 20))

        cross_matching_data = CrossMatching.objects.get(pk=pk)
        
        patient_info = [
            [
                Paragraph("<b>Name:</b>", styles["Normal"]),
                Paragraph(str(cross_matching_data.patient), styles["Normal"]),
                Paragraph("<b>Date:</b>", styles["Normal"]),
                Paragraph(datetime.now().strftime("%Y/%m/%d"), styles["Normal"]),
            ]
        ]

        patient_table = Table(
            patient_info, colWidths=[0.8 * inch, 4 * inch, 0.8 * inch, 2 * inch]
        )
        patient_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ]
            )
        )

        elements.append(patient_table)
        elements.append(Spacer(1, 20))

        data = [
            [
                "Serial No.",
                "Blood Type",
                "Amt. In cc.",
                "Blood Bank",
                "Date of Collection",
                "Expiration Date",
                "Result",
            ],
        ]

        for result in cross_matching_data.results.all():
            data.append(
                [
                    result.serial_no,
                    result.blood_bank,
                    result.amt_in_cc,
                    result.blood_bank,
                    result.date_of_collection.strftime("%Y/%m/%d"),
                    result.expiration_date.strftime("%Y/%m/%d"),
                    result.result,
                ]
            )

        main_table = Table(
            data,
            colWidths=[
                1 * inch,
                1 * inch,
                1 * inch,
                1.25 * inch,
                1.2 * inch,
                1.2 * inch,
                1 * inch,
            ],
        )
        main_table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 1, colors.black),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(main_table)
        elements.append(Spacer(1, 30))

        signatory_style = ParagraphStyle(
            "Signatory",
            parent=styles["Normal"],
            fontSize=12,
            alignment=1,
            spaceBefore=0,
            spaceAfter=0,
        )

        signatory_data = [
            [
                Paragraph(
                    f"<b>{cross_matching_data.medical_technologist.get_full_name()}</b>",
                    signatory_style,
                ),
                Paragraph(
                    f"<b>{cross_matching_data.pathologist.get_full_name()}</b>",
                    signatory_style,
                ),
            ],
            [
                Paragraph(f"Lic no. 124343", signatory_style),
                Paragraph(f"Lic no. 2434532", signatory_style),
            ],
            [
                Paragraph("<b>Pathologist</b>", signatory_style),
                Paragraph("<b>Medical Technologist</b>", signatory_style),
            ],
        ]

        signatory_table = Table(signatory_data, colWidths=[4 * inch, 4 * inch])
        signatory_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        filename = f"cross_matching_result_{slugify(cross_matching_data.patient)}_{datetime.now().strftime('%Y%m%d')}.pdf"
        elements.append(signatory_table)
        doc.title = "Cross Matching Result"
        doc.build(elements, onFirstPage=add_logo)
        buffer.seek(0)
        response = FileResponse(buffer, as_attachment=True, filename=filename)
        return response


def generate_rbs_result(request, pk):
    if request.method == "GET":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=0.5 * inch,
            leftMargin=1.1 * inch,
            rightMargin=1.1 * inch,
            bottomMargin=1 * inch,
        )

        elements = []
        styles = getSampleStyleSheet()
        styles["Normal"].fontSize = 12

        header_style = ParagraphStyle(
            "CustomHeader",
            parent=styles["Normal"],
            fontSize=12,
            alignment=1,
            spaceAfter=0,
            spaceBefore=0,
            leading=15,
            textColor=colors.black,
        )

        header_content = [
            [
                Paragraph(
                    "<b>PRESIDENT ROXAS PROVINCIAL COMMUNITY HOSPITAL</b><br/>"
                    "New Cebu, Pres. Roxas, Cotabato.<br/>"
                    "<b>LABORATORY DEPARTMENT</b><br/>",
                    header_style,
                ),
            ]
        ]

        header_table = Table(header_content, colWidths=[7.2 * inch])
        header_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                ]
            )
        )

        elements.append(header_table)
        elements.append(Spacer(1, 20))

        get_patient = Patient.objects.get(pk=pk)
        rbs_data = RBS.objects.get(patient=get_patient.pk)

        patient_info = [
            [
                Paragraph("<b>Name:</b>", styles["Normal"]),
                Paragraph(str(get_patient), styles["Normal"]),
                Paragraph("<b>Date:</b>", styles["Normal"]),
                Paragraph(datetime.now().strftime("%Y/%m/%d"), styles["Normal"]),
            ]
        ]

        header_table_labresult = Paragraph("<b>RBS</b>", header_style)
        elements.append(header_table_labresult)
        elements.append(Spacer(1, 20))

        patient_table = Table(
            patient_info, colWidths=[0.8 * inch, 4 * inch, 0.8 * inch, 2 * inch]
        )
        patient_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ]
            )
        )

        elements.append(patient_table)
        elements.append(Spacer(1, 20))

        data = [
            [
                "Results (mmol/dl)",
                "Date",
                "Time",
            ],
        ]

        for result in rbs_data.rbs_result.all():
            data.append(
                [
                    result.result,
                    result.get_date(),
                    result.get_time(),
                ]
            )

        main_table = Table(
            data,
            colWidths=[
                2.5 * inch,
                2.5 * inch,
                2.4 * inch,
            ],
        )
        main_table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 1, colors.black),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(main_table)
        elements.append(Spacer(1, 30))

        signatory_style = ParagraphStyle(
            "Signatory",
            parent=styles["Normal"],
            fontSize=12,
            alignment=1,
            spaceBefore=0,
            spaceAfter=0,
        )

        signatory_data = [
            [
                Paragraph(
                    f"<b>{rbs_data.assigned_pathologist.get_full_name()}</b>",
                    signatory_style,
                ),
                Paragraph(
                    f"<b>{rbs_data.assigned_technologist.get_full_name()}</b>",
                    signatory_style,
                ),
            ],
            [
                Paragraph(
                    f"Lic no. 12343",
                    signatory_style,
                ),
                Paragraph(
                    f"Lic no. 12343",
                    signatory_style,
                ),
            ],
            [
                Paragraph("<b>Pathologist</b>", signatory_style),
                Paragraph("<b>Medical Technologist</b>", signatory_style),
            ],
        ]

        signatory_table = Table(signatory_data, colWidths=[4 * inch, 4 * inch])
        signatory_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        filename = (
            f"rbs_result_{slugify(get_patient)}_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        elements.append(signatory_table)
        doc.title = "RBS Result"
        doc.build(elements, onFirstPage=add_logo)
        buffer.seek(0)
        response = FileResponse(buffer, as_attachment=True, filename=f"{filename}")
        return response
