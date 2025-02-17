from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    license_number = models.CharField(max_length=10, unique=True, db_index=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Patient(models.Model):
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, null=False, blank=True)
    lastname = models.CharField(max_length=255)

    age = models.PositiveIntegerField()
    sex = models.CharField(
        max_length=10, choices=(("Male", "Male"), ("Female", "Female"))
    )
    birthdate = models.DateField(help_text="Birth date of the patient", null=True, blank=True)
    address = models.TextField(help_text="Permanent address of the patient", null=True, blank=True)
    physician = models.ForeignKey(
        CustomUser,
        related_name="physician",
        limit_choices_to={"groups__name": "Physician"},
        on_delete=models.CASCADE,
    )
    room_number = models.PositiveIntegerField(null=True, blank=True, help_text="Leave room number as empty if out patient")
    sample_type = models.CharField(max_length=255)
    time_of_collection = models.TimeField(auto_now_add=True)
    date_of_collection = models.DateField(auto_now_add=True)
    sars_result = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    serial_number = models.CharField(max_length=255, help_text="Serial number example: PT-01152025-R23")
    assigned_pathologist = models.ForeignKey(
        CustomUser,
        related_name="patient_pathologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Pathologist"},
    )
    assigned_technologist = models.ForeignKey(
        CustomUser,
        related_name="patient_technologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Medical Technologist"},
    )

    patient_type = models.CharField(
        max_length=100,
        default="In Patient",
        choices=(
            ("In Patient", "In Patient"),
            ("Out Patient", "Out Patient"),
        ),
    )

    def get_full_name(self):
        return f"{self.firstname}  { self.middlename[0] + '.' if self.middlename else ''} {self.lastname}"

    def get_date(self):
        return self.date.strftime("%Y/%m/%d")

    def get_time_of_collection(self):
        return self.time_of_collection.strftime("%H:%M %p")

    def __str__(self) -> str:
        return f"Patient {self.get_full_name()}"

    class Meta:
        ordering = ("time_of_collection",)


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
    re_test = models.BooleanField(
        default=False, help_text="Re-test clinical chemistry results"
    )
    assigned_pathologist = models.ForeignKey(
        CustomUser,
        related_name="chemical_chemist_pathologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Pathologist"},
    )
    assigned_technologist = models.ForeignKey(
        CustomUser,
        related_name="chemical_chemist_technologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Medical Technologist"},
    )

    def __str__(self) -> str:
        return f"Clinical Chemistry Result of {self.patient} {self.date}"

    def get_date(self):
        return self.date.strftime("%Y/%m/%d")

    class Meta:
        verbose_name = "Clinical Chemistry"
        verbose_name_plural = "Clinical Chemistry"
        db_table = "clinical_chemistry"
        ordering = ("date",)


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
    re_test = models.BooleanField(default=False, help_text="Re-test Hematology")
    date = models.DateField(auto_now_add=True)

    assigned_pathologist = models.ForeignKey(
        CustomUser,
        related_name="assigned_pathologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Pathologist"},
    )
    assigned_technologist = models.ForeignKey(
        CustomUser,
        related_name="assigned_technologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Medical Technologist"},
    )

    def __str__(self) -> str:
        return f"Hematology Result of {self.patient} {self.date}"

    def get_date(self):
        return self.date.strftime("%m/%d/%Y")

    class Meta:
        verbose_name = "Hematology"
        verbose_name_plural = "Hematology"
        db_table = "hematology"
        ordering = ("date",)


class Serology(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_serology"
    )

    hb_determination = models.CharField(max_length=255)
    typhidot_rapid_test = models.CharField(max_length=255)
    dengue_rapid_test = models.CharField(max_length=255)
    re_test = models.BooleanField(default=False, help_text="Re-test serology")
    assigned_pathologist = models.ForeignKey(
        CustomUser,
        related_name="serology_pathologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Pathologist"},
    )
    assigned_technologist = models.ForeignKey(
        CustomUser,
        related_name="serology_technologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Medical Technologist"},
    )

    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Serology Result of {self.patient} {self.date}"

    def get_date(self):
        return self.date.strftime("%m/%d/%Y")


class CrossMatchingResult(models.Model):
    serial_no = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique serial number of the cross-matching result.",
    )
    amt_in_cc = models.FloatField(help_text="Amount in cc.")
    blood_bank = models.CharField(max_length=255, help_text="Name of the blood bank.")
    blood_type = models.CharField(max_length=255, help_text="Name of the blood type")
    date_of_collection = models.DateField(help_text="Date the blood was collected.")
    expiration_date = models.DateField(help_text="Expiration date of the blood.")
    result = models.TextField(max_length=255, help_text="Result of the cross-matching.")

    def __str__(self) -> str:
        return f"Result {self.serial_no} from {self.blood_bank}"

    class Meta:
        verbose_name = "Cross Matching Result"
        verbose_name_plural = "Cross Matching Results"
        db_table = "cross_matching_result"
        ordering = ["-date_of_collection"]


class CrossMatching(models.Model):
    results = models.ManyToManyField(
        CrossMatchingResult,
        related_name="cross_matchings",
        help_text="Related cross-matching results.",
    )
    patient = models.ForeignKey(
        "Patient",
        related_name="cross_matchings",
        on_delete=models.CASCADE,
        help_text="Patient associated with this cross-matching.",
    )
    pathologist = models.ForeignKey(
        CustomUser,
        related_name="pathologist_cross_matchings",
        limit_choices_to={"groups__name": "Pathologist"},
        on_delete=models.CASCADE,
        help_text="Pathologist overseeing the cross-matching.",
        null=True,
        blank=True,
    )
    medical_technologist = models.ForeignKey(
        CustomUser,
        related_name="technologist_cross_matchings",
        limit_choices_to={"groups__name": "Medical Technologist"},
        on_delete=models.CASCADE,
        help_text="Medical technologist handling the cross-matching.",
        null=True,
        blank=True,
    )
    re_test = models.BooleanField(default=False, help_text="Re-test the cross-matching")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp of record creation."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of last update."
    )

    def __str__(self) -> str:
        return f"Cross Matching for {self.patient} (Created: {self.created_at.date()})"

    class Meta:
        verbose_name = "Cross Matching"
        verbose_name_plural = "Cross Matchings"
        db_table = "cross_matching"
        ordering = ["-created_at"]


class RBSResult(models.Model):
    result = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)

    def __str__(self) -> str:
        return f"Result {self.result}"

    def get_time(self):
        return self.time.strftime("%I:%M %p")

    def get_date(self):
        return self.date.strftime("%m/%d/%Y")

    class Meta:
        ordering = ("date",)


class RBS(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_rbs"
    )
    rbs_result = models.ManyToManyField(
        RBSResult,
        related_name="rbs_results",
        help_text="Related RBS results.",
    )

    assigned_pathologist = models.ForeignKey(
        CustomUser,
        related_name="rbs_assigned_pathologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Pathologist"},
    )
    re_test = models.BooleanField(default=False, help_text="Retest the RBS")
    assigned_technologist = models.ForeignKey(
        CustomUser,
        related_name="rbs_assigned_technologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Medical Technologist"},
    )

    def __str__(self) -> str:
        return f"RBS Result of {self.patient}"


class Urinalysis(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_urinalysis"
    )
    color = models.CharField(max_length=255, help_text="Color")
    appearance = models.CharField(max_length=255, help_text="Appearance")
    specific_gravity = models.CharField(max_length=255, help_text="Specific Gravity")
    pH = models.CharField(max_length=255, help_text="pH")
    sugar = models.CharField(max_length=255, help_text="Sugar")
    albumin = models.CharField(max_length=255, help_text="Albumin")
    epithelia = models.CharField(max_length=255, help_text="Epithelia")
    bacteria = models.CharField(max_length=255, help_text="Bacteria")
    pus_cells = models.CharField(max_length=255, help_text="Pus Cells")
    rbc = models.CharField(max_length=255, help_text="RBC")
    cast = models.CharField(max_length=255, help_text="Cast")
    crystals = models.CharField(max_length=255, help_text="Crystals")
    others = models.CharField(max_length=255, help_text="Others")
    amorphous = models.CharField(max_length=255, help_text="Amorphous")
    mucous_thread = models.CharField(max_length=255, help_text="Mucous Thread")
    pregnancy_test = models.CharField(
        max_length=255, help_text="Pregnancy Test", null=True, blank=True
    )
    re_test = models.BooleanField(default=False, help_text="Re-test urinalysis")
    urates = models.CharField(max_length=255, help_text="Urates", null=True, blank=True)

    assigned_pathologist = models.ForeignKey(
        CustomUser,
        related_name="urinalysis_assigned_pathologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Pathologist"},
        help_text="Pathologist name",
    )
    assigned_technologist = models.ForeignKey(
        CustomUser,
        related_name="urinalysis_assigned_technologist",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"groups__name": "Medical Technologist"},
        help_text="Medical Technologist name",
    )

    date = models.DateField(auto_now_add=True)

    def get_date(self):
        return self.date.strftime("%m/%d/%Y")

    def __str__(self) -> str:
        return f"Urinalysis Result of {self.patient} {self.date}"

    class Meta:
        ordering = ("date",)


class LabRequest(models.Model):
    lab_request_type = (
        ("Clinical Chemistry", "Clinical Chemistry"),
        ("Cross Matching", "Cross Matching"),
        ("Urinalysis", "Urinalysis"),
        ("Hematology", "Hematology"),
        ("Serology", "Serology"),
        ("RBS", "RBS"),
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="patient_lab_requests",
        help_text="Patient needs to be examine",
    )
    description = models.TextField(
        max_length=300, help_text="Description for laboratory request"
    )
    lab_request_type = models.CharField(
        max_length=255,
        choices=lab_request_type,
        help_text="Type of laboratory request",
    )

    requested_by = models.ForeignKey(
        CustomUser,
        related_name="requested_by_lab",
        limit_choices_to=Q(groups__name="Doctor") | Q(groups__name="Nurse"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_request = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(
        default=False, help_text="Toggle if the request is done."
    )

    def __str__(self) -> str:
        return f"Lab Request for {self.patient} laboratory request for {self.lab_request_type}"

    def get_datetime_request(self):
        return self.date_request.strftime("%m/%d/%Y %I:%M %p")
