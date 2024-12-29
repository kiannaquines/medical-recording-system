from django.apps import AppConfig


class HospitalAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_app'
    verbose_name = 'Hospital Patient Information'

    def ready(self):
        import hospital_app.signals
