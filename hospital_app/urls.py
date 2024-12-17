from django.urls import path
from hospital_app.views import *
from hospital_app.create_view import *
from hospital_app.delete_view import *
from hospital_app.update_view import *

urlpatterns = [
    path('', LoginView.as_view(), name="login"),

    # View
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('patient/', PatientListView.as_view(), name="patient_list"),
    path('employee/', EmployeeListView.as_view(), name="employee_list"),
    path('laboratory/chemical-chemistry/result', ClinicalChemistryView.as_view(), name="chemical_chemistry_list"),
    path('laboratory/serology/result', SerologyView.as_view(), name="serology_list"),
    path('laboratory/hematology/result', HematologyView.as_view(), name="hematology_list"),
    path('laboratory/cross-matching/result', CrossMatchingView.as_view(), name="cross_matching_list"),
    path('laboratory/cross-matching-result/result', CrossMatchingResultView.as_view(), name="cross_matching_result_list"),

    # Create
    path('laboratory/hematology/add', HematologyCreateView.as_view(), name="hematology_add"),
    path('laboratory/serology/add', SerologyCreateView.as_view(), name="serology_add"),
    path('laboratory/clinical-chemistry/add', ClinicalChemicalCreateView.as_view(), name="clinical_chemistry_add"),
    path('laboratory/cross-matching/add', CrossMatchingChemicalCreateView.as_view(), name="cross_matching_add"),
    path('laboratory/cross-matching-result/add', CrossMatchingResultCreateView.as_view(), name="cross_matching_result_add"),
    path('patient/add', PatientCreateView.as_view(), name="patient_add"),
    path('employee/add', EmployeeCreateView.as_view(), name="employee_add"),

    # Update
    path('laboratory/hematology/update/<int:pk>', HematologyUpdateView.as_view(), name="hematology_update"),
    path('laboratory/serology/update/<int:pk>', SerologyUpdateView.as_view(), name="serology_update"),
    path('laboratory/clinical-chemistry/update/<int:pk>', ClinicalChemicalUpdateView.as_view(), name="clinical_chemistry_update"),
    path('laboratory/cross-matching/update/<int:pk>', CrossMatchingUpdateView.as_view(), name="cross_matching_update"),
    path('laboratory/cross-matching-result/update/<int:pk>', CrossMatchingResultUpdateView.as_view(), name="cross_matching_result_update"),
    path('patient/update/<int:pk>', PatientUpdateView.as_view(), name="patient_update"),
    path('employee/update/<int:pk>', EmployeeUpdateView.as_view(), name="employee_update"),

    # Delete
    path('laboratory/hematology/delete/<int:pk>', HematologyDeleteView.as_view(), name="hematology_delete"),
    path('laboratory/serology/delete/<int:pk>', SerologyDeleteView.as_view(), name="serology_delete"),
    path('laboratory/clinical-chemistry/delete/<int:pk>', ClinicalChemicalDeleteView.as_view(), name="clinical_chemistry_delete"),
    path('laboratory/cross-matching/delete/<int:pk>', CrossMatchingDeleteView.as_view(), name="cross_matching_delete"),
    path('laboratory/cross-matching-result/delete/<int:pk>', CrossMatchingResultDeleteView.as_view(), name="cross_matching_result_delete"),
    path('patient/delete/<int:pk>', PatientDeleteView.as_view(), name="patient_delete"),
    path('employee/delete/<int:pk>', EmployeeDeleteView.as_view(), name="employee_delete"),

    # Export
]