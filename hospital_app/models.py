from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class EmployeeInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10, unique=True, db_index=True)

    def __str__(self):
        return f"{self.user.get_full_name()}{self.license_number}"


class Patient(models.Model):
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    age = models.PositiveIntegerField()
    sex = models.CharField(
        max_length=10, choices=(("Male", "Male"), ("Female", "Female"))
    )
    physician = models.ForeignKey(
        User,
        related_name="physician",
        limit_choices_to={"groups__name": "Physician"},
        on_delete=models.CASCADE,
    )
    room_number = models.PositiveIntegerField()
    sample_type = models.CharField(max_length=255)
    time_of_collection = models.TimeField()
    date_of_collection = models.DateField()
    sars_result = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    assigned_pathologist = models.ForeignKey(User, related_name="patient_pathologist", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'groups__name':'Pathologist'})
    assigned_technologist = models.ForeignKey(User, related_name="patient_technologist", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'groups__name':'Medical Technologist'})

    def get_full_name(self):
        return f"{self.firstname} {self.middlename} {self.lastname}"

    def __str__(self) -> str:
        return self.get_full_name()

class ClinicalChemistry(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_clinical_chemistry"
    )

    glucose = models.FloatField()
    cholesterol = models.FloatField()
    triglycerides = models.FloatField()
    hdl = models.FloatField()
    ldl = models.FloatField()
    creatinine = models.FloatField()
    uric_acid = models.FloatField()
    bun = models.FloatField()
    sgpt = models.FloatField()
    sgot = models.FloatField()
    date = models.DateField(auto_now_add=True)


    assigned_pathologist = models.ForeignKey(User, related_name="chemical_chemist_pathologist", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'groups__name':'Pathologist'})
    assigned_technologist = models.ForeignKey(User, related_name="chemical_chemist_technologist", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'groups__name':'Medical Technologist'})

    def __str__(self) -> str:
        return f"Clinical Chemistry Result of {self.patient} {self.date}"

    def get_date(self):
        return self.date.strftime("%Y/%m/%d")

    class Meta:
        verbose_name = "Clinical Chemistry"
        verbose_name_plural = "Clinical Chemistry"
        db_table = "clinical_chemistry"

class Hematology(models.Model):

    BLOOD_TYPE_CHOICES = (
        ("A+", "A Positive"),
        ("A-", "A Negative"),
        ("B+", "B Positive"),
        ("B-", "B Negative"),
        ("AB+", "AB Positive"),
        ("AB-", "AB Negative"),
        ("O+", "O Positive"),
        ("O-", "O Negative"),
    )

    RH_TYPE_CHOICES = (
        ("+ (Positive)", "Positive"),
        ("- (Negative)", "Negative"),
    )

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_hematology"
    )

    hemoglobin_mass_concentration = models.CharField(max_length=255)
    hematocrit = models.CharField(max_length=255)
    erythrocty_no_concentration = models.CharField(max_length=255)
    platelet = models.IntegerField()

    blood_type = models.CharField(max_length=255, choices=BLOOD_TYPE_CHOICES)
    rh_type = models.CharField(max_length=255, choices=RH_TYPE_CHOICES)

    leucocyte_no_concentration = models.FloatField()
    segmenters = models.CharField(max_length=255)
    lymphocytes = models.FloatField()
    monocytes = models.FloatField()
    eosinophils = models.FloatField()
    basophils = models.FloatField()
    date = models.DateField(auto_now_add=True)

    assigned_pathologist = models.ForeignKey(User, related_name="assigned_pathologist", on_delete=models.CASCADE, null=False, blank=False, limit_choices_to={'groups__name':'Pathologist'})
    assigned_technologist = models.ForeignKey(User, related_name="assigned_technologist", on_delete=models.CASCADE, null=False, blank=False, limit_choices_to={'groups__name':'Medical Technologist'})

    def __str__(self) -> str:
        return f"Hematology Result of {self.patient} {self.date}"

    def get_date(self):
        return self.date.strftime("%m/%d/%Y")

    class Meta:
        verbose_name = "Hematology"
        verbose_name_plural = "Hematology"
        db_table = "hematology"

class Serology(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_serology"
    )

    hb_determination = models.CharField(max_length=255)
    typhidot_rapid_test = models.CharField(max_length=255)
    dengue_rapid_test = models.CharField(max_length=255)

    assigned_pathologist = models.ForeignKey(User, related_name="serology_pathologist", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'groups__name':'Pathologist'})
    assigned_technologist = models.ForeignKey(User, related_name="serology_technologist", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'groups__name':'Medical Technologist'})

    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Serology Result of {self.patient} {self.date}"
    

    def get_date(self):
        return self.date.strftime("%m/%d/%Y")

class CrossMatchingResult(models.Model):
    amt_in_cc = models.FloatField()
    blood_bank = models.CharField(max_length=255)
    date_of_collection = models.DateField()
    expiration_date = models.DateField()
    result = models.TextField(max_length=255)

    def __str__(self) -> str:
        return f"Cross Matching Result {self.date_of_collection}"

    class Meta:
        verbose_name = "Cross Matching Result"
        verbose_name_plural = "Cross Matching Result"
        db_table = "cross_matching_result"

class CrossMatching(models.Model):
    result = models.ForeignKey(
        CrossMatchingResult,
        on_delete=models.CASCADE,
        related_name="cross_matching_result",
        help_text="Result of cross matching",
    )
    patient = models.ForeignKey(
        "Patient",
        related_name="patient_cross_matching_result",
        on_delete=models.CASCADE,
        help_text="Patient name",
    )
    pathologist = models.ForeignKey(
        User,
        related_name="pathologist",
        limit_choices_to={"groups__name": "Pathologist"},
        on_delete=models.CASCADE,
        help_text="Pathologist name",
    )
    medical_technologist = models.ForeignKey(
        User,
        related_name="medical_technologist",
        limit_choices_to={"groups__name": "Medical Technologist"},
        on_delete=models.CASCADE,
        help_text="Medical Technologist name",
    )

    def __str__(self) -> str:
        return f"Cross Matching Result of {self.patient}"

    class Meta:
        verbose_name = "Cross Matching"
        verbose_name_plural = "Cross Matching"
        db_table = "cross_matching"
