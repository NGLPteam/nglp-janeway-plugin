from django import apps
from django.core import signals



class NGLPConfig(apps.AppConfig):
    name = "nglp"
    verbose_name = "NGLP"

    @property
    def analytics_url(self):
        from django.conf import settings
        return settings.NGLP_ANALYTICS_URL

    def ready(self):
        from utils.models import LogEntry
