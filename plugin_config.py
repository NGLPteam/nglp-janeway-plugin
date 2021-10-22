from events.logic import Events

NGLP_ANALYTICS_API = "http://127.0.0.1:8002/api/"

NGLP_ANALYTICS_EVENT_CONFIG = {
    Events.ON_ARTICLE_SUBMITTED: "submit",
    Events.ON_REVIEW_COMPLETE: "review",
    Events.ON_ARTICLE_ACCEPTED: "accept",
    Events.ON_ARTICLE_PUBLISHED: "publish"
    }