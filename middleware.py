from http import HTTPStatus

from django.apps import apps
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import ResolverMatch

from core import models as core_models
from submission import models as submission_models




class NGLPMiddleware(MiddlewareMixin):
    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        resolver_match: ResolverMatch = request.resolver_match
        if not resolver_match:
            return response

        if resolver_match.url_name == 'journal_file' and response.status_code == HTTPStatus.OK.value:
            file = core_models.File.objects.get(pk=resolver_match.kwargs["file_id"])
            article: submission_models.Article = file.article

            event = {
                'event': 'request',
                'object_type': 'File',
                'object_id': list(filter(None, [article.get_identifier('pubid'), article.get_doi()])),
                'format': file.mime_type,
                'url': request.build_absolute_uri(),
                'referrer': request.META.get('HTTP_REFERRER'),
                'user_agent': request.META.get('HTTP_USER_AGENT'),
                'ip' : request.META.get('REMOTE_ADDR')
                # FIXME: Talk to Richard about how pseudoanonymised he wants the IPs to be, and when

            }

            # TODO: Send event to API
            apps.get_app_config("nglp").send_event(event)

        return response
