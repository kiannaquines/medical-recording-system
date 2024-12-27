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
        context["logs"] = LogEntry.objects.select_related(
            "user", "content_type"
        ).order_by("-action_time")
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


class RBSView(ListView):
    template_name = "rbs.html"
    queryset = RBS.objects.all()
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail_header"] = "RBS Details List"
        context["humberger_header"] = "RBS Details"
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


def generate_urinalysis_result(request, pk):
    if request.method == "GET":
        try:
            urinalysis_detail = get_object_or_404(Urinalysis, pk=pk)
            assigned_technologist_details = get_object_or_404(
                EmployeeInfo, user=urinalysis_detail.assigned_technologist
            )
            assigned_pathologistlogist_details = get_object_or_404(
                EmployeeInfo, user=urinalysis_detail.assigned_technologist
            )

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
                "name1": assigned_pathologistlogist_details.user.get_full_name(),
                "name2": assigned_technologist_details.user.get_full_name(),
                "lic1": assigned_pathologistlogist_details.license_number,
                "lic2": assigned_technologist_details.license_number,
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

            response = FileResponse(filled_pdf_buffer, content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="urinalysis_{pk}.pdf"'
            )
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
        technologist = get_object_or_404(
            EmployeeInfo, user=cross_matching_data.medical_technologist
        )
        pathologist = get_object_or_404(
            EmployeeInfo, user=cross_matching_data.pathologist
        )
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
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, colors.black),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, colors.black),
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
                Paragraph(f"Lic no. {technologist.license_number}", signatory_style),
                Paragraph(f"Lic no. {pathologist.license_number}", signatory_style),
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
                    "<b>LABORATORY DEPARTMENT</b><br/>"
                    "<b>RBS</b>",
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

        rbs_data = RBS.objects.filter(patient=get_patient.pk)

        patient_info = [
            [
                Paragraph("<b>Name:</b>", styles["Normal"]),
                Paragraph(str(get_patient), styles["Normal"]),
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
                "Results (mmol/dl)",
                "Date",
                "Time",
            ],
        ]

        for result in rbs_data:
            data.append(
                [
                    result.result,
                    result.date,
                    result.time,
                ]
            )

        main_table = Table(
            data,
            colWidths=[
                2.4 * inch,
                2.4 * inch,
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

        # signatory_data = [
        #     [
        #         Paragraph(
        #             f"<b>{technologist.user.get_full_name()}</b>",
        #             signatory_style,
        #         ),
        #         Paragraph(
        #             f"<b>{pathologist.user.get_full_name()}</b>",
        #             signatory_style,
        #         ),
        #     ],
        #     [
        #         Paragraph(f"Lic no. {technologist.license_number}", signatory_style),
        #         Paragraph(f"Lic no. {pathologist.license_number}", signatory_style),
        #     ],
        #     [
        #         Paragraph("<b>Pathologist</b>", signatory_style),
        #         Paragraph("<b>Medical Technologist</b>", signatory_style),
        #     ],
        # ]

        # signatory_table = Table(signatory_data, colWidths=[4 * inch, 4 * inch])
        # signatory_table.setStyle(
        #     TableStyle(
        #         [
        #             ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        #             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        #         ]
        #     )
        # )

        # filename = f"rbs_result_{slugify(cross_matching_data.patient)}_{datetime.now().strftime('%Y%m%d')}.pdf"
        # elements.append(signatory_table)
        doc.title = "RBS Result"
        doc.build(elements, onFirstPage=add_logo)
        buffer.seek(0)
        response = FileResponse(buffer, as_attachment=True, filename="filename.pdf")
        return response
