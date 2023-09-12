from django.apps import AppConfig


class AdditionalcostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calculator_projects.apps.additionalCosts"

    def ready(self):
        import calculator_projects.apps.additionalCosts.signals
