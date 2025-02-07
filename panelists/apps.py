from django.apps import AppConfig


class PanelistsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "panelists"

    def ready(self):
        import panelists.signals
