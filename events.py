from http import HTTPStatus

from django.apps import apps
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import ResolverMatch
from django.conf import settings
import mimetypes

from core import models as core_models
from submission.models import Article
from metrics.models import ArticleAccess

ACCESS_TYPE_MAPPING = {
    "download": "request",
    "view": "investigation",
}


def on_article_access(article: Article, article_access: ArticleAccess, request: HttpRequest, **kwargs):
    # event type is mapped either download (request) or view (investigation)

    # can't log journal or issue views at present. We need to go and find where/if we can access them.
    try:
        event_type = ACCESS_TYPE_MAPPING[article_access.type]
    except KeyError:
        return

    event = {
        "event": event_type,
        "object_type": "File",
        "object_id": list(
            filter(None, [article.get_identifier("pubid"), article.get_doi()])
        ),

        # FIXME: Need to ask Janeway if we need to anonymise IPs. Ask Andy
    }
    if article_access.galley_type != "view":
        event["format"] = mimetypes.types_map.get('.' + article_access.galley_type, 'application/octet-stream'),

    return send_event(event=event, request=request)

def send_event(*, event, request):
    event = {
        'url': request.build_absolute_uri(),
        'referrer': request.META.get('HTTP_REFERRER'),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
        'ip' : request.META.get('REMOTE_ADDR'),
        **event,
    }

    try:
        response = requests.post(settings.NGLP_ANALYTICS_API, data=json.dumps(event))
        response.raise_for_status()
    except requests.exceptions.RequestException:
        logger.exception(msg="failed to send event.")

