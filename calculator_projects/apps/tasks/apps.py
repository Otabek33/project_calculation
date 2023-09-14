from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calculator_projects.apps.tasks"

    def ready(self):
        import calculator_projects.apps.tasks.signals
