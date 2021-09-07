from http import HTTPStatus

from django.apps import apps
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import ResolverMatch

from core import models as core_models
from submission import models as submission_models


class NGLPMiddleware(MiddlewareMixin):
    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        resolver_match: ResolverMatch = request.resolver_match
        if not resolver_match:
            return response

        if (
            resolver_match.url_name == "journal_file"
            and response.status_code == HTTPStatus.OK.value
        ):
            file = core_models.File.objects.get(pk=resolver_match.kwargs["file_id"])
            article: submission_models.Article = file.article

            event = {
                "event": "request",
                "object_type": "File",
                "object_id": list(
                    filter(None, [article.get_identifier("pubid"), article.get_doi()])
                ),
                "format": file.mime_type,
                # FIXME: Need to ask Janeway if we need to anonymise IPs. Ask Andy
            }

            # if resolver_match.url_name == 'article_download_galley'  and response.status_code == HTTPStatus.OK.value:
            #     galley = core_models.Galley.objects.get(pk=galley_id)

            # TODO: Send event to API
            apps.get_app_config("nglp").send_event(event=event, request=request)

        return response
