from django.http import HttpResponse as BaseHttpResponse
from django_htmx.middleware import HtmxDetails


class HttpResponse(BaseHttpResponse):
    htmx: HtmxDetails


__all__ = ["HttpResponse"]
