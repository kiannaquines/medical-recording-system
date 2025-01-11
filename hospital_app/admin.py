from django.contrib import admin
from hospital_app.models import *
from django.contrib.auth.admin import UserAdmin as OriginalAdmin
from django.utils.translation import gettext_lazy as _



class CustomUserAdmin(OriginalAdmin):
    list_display = ('username', 'email', 'date_joined',)
    fieldsets = (
        (None, {"fields": ("username", "password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email","license_number",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_filter = ('date_joined', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

admin.site.register(CustomUser, CustomUserAdmin)

hospital_models = [
    Patient,
    ClinicalChemistry,
    Hematology,
    Serology,
    CrossMatchingResult,
    CrossMatching,
    RBS,
    Urinalysis,
    LabRequest,
]

for model in hospital_models:
    admin.site.register(model)