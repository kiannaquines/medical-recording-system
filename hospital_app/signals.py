from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

from .models import (
    EmployeeInfo, Patient, ClinicalChemistry, Hematology,
    Serology, CrossMatching, RBS, Urinalysis
)

MODELS_TO_LOG = [
    EmployeeInfo,
    Patient,
    ClinicalChemistry,
    Hematology,
    Serology,
    CrossMatching,
    RBS,
    Urinalysis,
]

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    if sender in MODELS_TO_LOG:
        action_flag = ADDITION if created else CHANGE
        LogEntry.objects.log_action(
            user_id=instance.assigned_pathologist_id if hasattr(instance, 'assigned_pathologist_id') else None,
            content_type_id=ContentType.objects.get_for_model(sender).pk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=action_flag,
            change_message=f"{'Created' if created else 'Updated'}: {instance}",
        )

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    if sender in MODELS_TO_LOG:
        LogEntry.objects.log_action(
            user_id=instance.assigned_pathologist_id if hasattr(instance, 'assigned_pathologist_id') else None,
            content_type_id=ContentType.objects.get_for_model(sender).pk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=DELETION,
            change_message=f"Deleted: {instance}",
        )
