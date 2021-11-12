from events.logic import Events
from django.conf import settings


NGLP_ANALYTICS_API = settings.NGLP_ANALYTICS_API

NGLP_ANALYTICS_EVENT_CONFIG = {
    Events.ON_ARTICLE_SUBMITTED: "submit",
    Events.ON_REVIEW_COMPLETE: "review",
    Events.ON_ARTICLE_ACCEPTED: "accept",
    Events.ON_ARTICLE_PUBLISHED: "publish"
    }