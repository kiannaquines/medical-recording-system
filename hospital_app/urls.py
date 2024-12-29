from django.urls import path
from hospital_app.views import *
from hospital_app.create_view import *
from hospital_app.delete_view import *
from hospital_app.update_view import *

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('logout/', logout_user, name="logout_user"),
    # View
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('patient/', PatientListView.as_view(), name="patient_list"),
    path('employee/', EmployeeListView.as_view(), name="employee_list"),
    path('laboratory/chemical-chemistry/result', ClinicalChemistryView.as_view(), name="chemical_chemistry_list"),
    path('laboratory/serology/result', SerologyView.as_view(), name="serology_list"),
    path('laboratory/hematology/result', HematologyView.as_view(), name="hematology_list"),
    path('laboratory/cross-matching/result', CrossMatchingView.as_view(), name="cross_matching_list"),
    path('laboratory/cross-matching-result/result', CrossMatchingResultView.as_view(), name="cross_matching_result_list"),
    path('laboratory/rbs/result', RBSView.as_view(), name="rbs_result_list"),
    path('laboratory/urinalysis/result', UrinalysisView.as_view(), name="urinalysis_result_list"),
    path('laboratory/rbs-result/result', PatientRBSView.as_view(), name="rbs__result_list"),
    # Create
    path('laboratory/hematology/add', HematologyCreateView.as_view(), name="hematology_add"),
    path('laboratory/serology/add', SerologyCreateView.as_view(), name="serology_add"),
    path('laboratory/clinical-chemistry/add', ClinicalChemicalCreateView.as_view(), name="clinical_chemistry_add"),
    path('laboratory/cross-matching/add', CrossMatchingChemicalCreateView.as_view(), name="cross_matching_add"),
    path('laboratory/cross-matching-result/add', CrossMatchingResultCreateView.as_view(), name="cross_matching_result_add"),
    path('patient/add', PatientCreateView.as_view(), name="patient_add"),
    path('employee/add', EmployeeCreateView.as_view(), name="employee_add"),
    path('employee/info/add/<int:pk>', employee_info_add_view, name="employee_info_add"),
    path('laboratory/rbs/add', RBSCreateView.as_view(), name="rbs_add"),
    path('laboratory/urinalysis/add', UrinalysisCreateView.as_view(), name="urinalysis_add"),
    path('laboratory/rbs-result/add', RBSResultCreateView.as_view(), name="rbs_result_add"),
    # Update
    path('laboratory/hematology/update/<int:pk>', HematologyUpdateView.as_view(), name="hematology_update"),
    path('laboratory/serology/update/<int:pk>', SerologyUpdateView.as_view(), name="serology_update"),
    path('laboratory/clinical-chemistry/update/<int:pk>', ClinicalChemicalUpdateView.as_view(), name="clinical_chemistry_update"),
    path('laboratory/cross-matching/update/<int:pk>', CrossMatchingUpdateView.as_view(), name="cross_matching_update"),
    path('laboratory/cross-matching-result/update/<int:pk>', CrossMatchingResultUpdateView.as_view(), name="cross_matching_result_update"),
    path('patient/update/<int:pk>', PatientUpdateView.as_view(), name="patient_update"),
    path('employee/update/<int:pk>', EmployeeUpdateView.as_view(), name="employee_update"),
    path('laboratory/rbs/update/<int:pk>', RBSUpdateView.as_view(), name="rbs_update"),
    path('laboratory/urinalysis/update/<int:pk>', UrinalysisUpdateView.as_view(), name="urinalysis_update"),
    path('laboratory/rbs-result/update/<int:pk>', RBSResultUpdateView.as_view(), name="rbs_result_update"),
    # Delete
    path('laboratory/hematology/delete/<int:pk>', HematologyDeleteView.as_view(), name="hematology_delete"),
    path('laboratory/serology/delete/<int:pk>', SerologyDeleteView.as_view(), name="serology_delete"),
    path('laboratory/clinical-chemistry/delete/<int:pk>', ClinicalChemicalDeleteView.as_view(), name="clinical_chemistry_delete"),
    path('laboratory/cross-matching/delete/<int:pk>', CrossMatchingDeleteView.as_view(), name="cross_matching_delete"),
    path('laboratory/cross-matching-result/delete/<int:pk>', CrossMatchingResultDeleteView.as_view(), name="cross_matching_result_delete"),
    path('patient/delete/<int:pk>', PatientDeleteView.as_view(), name="patient_delete"),
    path('employee/delete/<int:pk>', EmployeeDeleteView.as_view(), name="employee_delete"),
    path('laboratory/rbs/delete/<int:pk>', RBSDeleteView.as_view(), name="rbs_delete"),
    path('laboratory/urinalysis/delete/<int:pk>', UrinalysisDeleteView.as_view(), name="urinalysis_delete"),
    path('laboratory/rbs-result/delete/<int:pk>', RBSResultDeleteView.as_view(), name="rbs_result_delete"),
    # Export
    path('generate-chemistry-result/<int:pk>', generate_chemistry_result, name="generate_chemistry_result"),
    path('generate-hematology-result/<int:pk>', generate_hematology_result, name="generate_hematology_result"),
    path('generate-serology-result/<int:pk>', generate_serology_result, name="generate_serology_result"),
    path('generate-panbio-result/<int:pk>', generate_panbio, name="generate_panbio"),
    path('generate-urinalysis-result/<int:pk>', generate_urinalysis_result, name="generate_urinalysis_result"),
    path('generate-cross-matching-result/<int:pk>', generate_cross_matching_result, name="generate_cross_matching_result"),
    path('generate-rbs-result/<int:pk>', generate_rbs_result, name="generate_rbs_result"),
]