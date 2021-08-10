import json
import logging

from django import apps
from django.core import signals
import requests
import requests.exceptions

logger = logging.getLogger(__name__)


class NGLPConfig(apps.AppConfig):
    name = "nglp"
    verbose_name = "NGLP"

    @property
    def analytics_url(self):
        from django.conf import settings
        return settings.NGLP_ANALYTICS_API

    def ready(self):
        from utils.models import LogEntry

    def send_event(self, event):
        # put event into JSON
        # POST request
        # find api endpoint

        try:
            response = requests.post(self.analytics_url, data=json.dumps(event))
            response.raise_for_status()
        except requests.exceptions.RequestException:
            logger.exception(msg="failed to send event.")
