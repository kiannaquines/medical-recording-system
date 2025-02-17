from django import forms
from hospital_app.models import *
from django.contrib.auth.forms import UserCreationForm

hospital_models = [
    Patient,
    ClinicalChemistry,
    Hematology,
    Serology,
    CrossMatchingResult,
    CrossMatching,
    RBS,
    Urinalysis,
    RBSResult,
    LabRequest,
]

custom_fields = {
    "date_of_collection": forms.DateInput(
        attrs={"type": "date", "class": "form-control"}
    ),
    "expiration_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),

    "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    "time": forms.DateInput(attrs={"type": "time", "class": "form-control"}),

    "time_of_collection": forms.TimeInput(
        attrs={"type": "time", "class": "form-control"}
    ),
    "re_test": forms.CheckboxInput(
        attrs={"type": "checkbox", "class": "form-check-input"}
    ),
    "is_done": forms.CheckboxInput(
        attrs={"type": "checkbox", "class": "form-check-input"}
    ),
    "birthdate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
}


class LaboratoryRequestFormNurseAndDoctor(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = LabRequest
        fields = ("patient", "description", "lab_request_type")
        exclude = ("requested_by","is_done")


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )


class EmployeeCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields_required = {
            "groups",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "license_number",
        }

        for field_name in fields_required:
            self.fields[field_name].required = True

        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "groups",
            "is_active",
            "is_staff",
            "is_superuser",
            "license_number",
        ]


class EmployeeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "groups",
            "is_active",
            "is_staff",
            "is_superuser",
            "license_number",
        ]


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_custom_widgets()

    def add_custom_widgets(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

            if field_name == "middlename" or field_name == "room_number":
                field.widget.attrs.update({"required": False})
            else:
                field.widget.attrs.update({"required": True})

            if field_name in custom_fields:
                self.fields[field_name].widget = custom_fields[field_name]
            else:
                if isinstance(field, forms.DateField):
                    field.widget.attrs.update({"type": "date"})
                if isinstance(field, forms.CheckboxInput):
                    field.widget.attrs.update({"class": "form-check-input"})
                elif isinstance(field, forms.TimeField):
                    field.widget.attrs.update({"type": "time"})


for model in hospital_models:
    form_class = type(
        f"{model.__name__}Form",
        (BaseForm,),
        {
            "Meta": type(
                "Meta",
                (),
                {
                    "model": model,
                    "fields": "__all__",
                },
            ),
        },
    )

    globals()[f"{model.__name__}Form"] = form_class
