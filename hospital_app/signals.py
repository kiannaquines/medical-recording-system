from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .models import (
    Patient, ClinicalChemistry, Hematology,
    Serology, CrossMatching, RBS, Urinalysis, LabRequest
)

MODELS_TO_LOG = [
    Patient,
    ClinicalChemistry,
    Hematology,
    Serology,
    CrossMatching,
    RBS,
    Urinalysis,
    LabRequest,
]

def get_user_from_instance(instance):
    if hasattr(instance, 'assigned_pathologist') and instance.assigned_pathologist:
        return instance.assigned_pathologist.pk
    
    if hasattr(instance, 'user') and instance.user:
        return instance.user.pk
    
    if hasattr(instance, 'requested_by') and instance.requested_by:
        return instance.requested_by.pk

    try:
        return settings.DEFAULT_SYSTEM_USER_ID
    except AttributeError:
        raise ValueError("DEFAULT_SYSTEM_USER_ID is not set in settings.")

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    if sender in MODELS_TO_LOG:
        action_flag = ADDITION if created else CHANGE
        try:
            user_id = get_user_from_instance(instance)
            LogEntry.objects.log_action(
                user_id=user_id,
                content_type_id=ContentType.objects.get_for_model(sender).pk,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=action_flag,
                change_message=f"{'Created' if created else 'Updated'}: {instance}",
            )
        except ValueError as e:
            print(f"Error logging save action: {e}")

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    if sender in MODELS_TO_LOG:
        try:
            user_id = get_user_from_instance(instance)
            LogEntry.objects.log_action(
                user_id=user_id,
                content_type_id=ContentType.objects.get_for_model(sender).pk,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=DELETION,
                change_message=f"Deleted: {instance}",
            )
        except ValueError as e:
            print(f"Error logging delete action: {e}")
