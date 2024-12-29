from django.contrib import admin
from hospital_app.models import *

hospital_models = [
    Patient,
    ClinicalChemistry,
    Hematology,
    Serology,
    CrossMatchingResult,
    CrossMatching,
    EmployeeInfo,
    RBS,
    Urinalysis,
    LabRequest,
]

for model in hospital_models:
    admin.site.register(model)