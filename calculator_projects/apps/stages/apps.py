from django.apps import AppConfig


class StagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calculator_projects.apps.stages"

    def ready(self):
        import calculator_projects.apps.stages.signals
