from http import HTTPStatus

from django.apps import apps
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import ResolverMatch
from django.conf import settings
import mimetypes
import requests
import json
from logging import Logger

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

def on_article_submitted(article: Article, request: HttpRequest, **kwargs):
    # When an article is submitted for review by an author
    event = {
      "event": "submit",
      "object_type": "Article",
      "object_id": list(
          filter(None, [article.identifier.identifier,
                        article.get_identifier("pubid"),
                        article.get_identifier("id"),
                        article.get_identifier("uri"),
                        article.get_doi()])
      )
    }

    return send_event(event=event, request=request)

def on_review_complete():
    # When an article review has been completed
    event = {
        "event": "review",
        "object_type": "Article",
        "object_id": list(
            filter(None, [article.identifier.identifier,
                          article.get_identifier("pubid"),
                          article.get_identifier("id"),
                          article.get_identifier("uri"),
                          article.get_doi()])
        )
    }

    return send_event(event=event, request=request)


def on_article_accepted():
    # When an article is accepted for publication
    event = {
      "event": "accept",
      "object_type": "Article",
      "object_id": list(
          filter(None, [article.identifier.identifier,
                        article.get_identifier("pubid"),
                        article.get_identifier("id"),
                        article.get_identifier("uri"),
                        article.get_doi()])
      )
    }

    return send_event(event=event, request=request)


def on_article_published():
    # When an article is published by a journal
    event = {
      "event": "publish",
      "object_type": "Article",
      "object_id": list(
          filter(None, [article.identifier.identifier,
                        article.get_identifier("pubid"),
                        article.get_identifier("id"),
                        article.get_identifier("uri"),
                        article.get_doi()])
      )
    }

    return send_event(event=event, request=request)


def on_article_declined():
    pass



def send_event(*, event, request):
    event = {
        'user_id': request.META.get('USER'),
        **event,
    }

    try:
        response = requests.post(settings.NGLP_ANALYTICS_API, data=json.dumps(event))
        response.raise_for_status()
    except requests.exceptions.RequestException:
        Logger.exception(msg="failed to send event.")


