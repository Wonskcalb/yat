from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from ninja import NinjaAPI


api = NinjaAPI(
    title="YAT API",
    description="API documentation to control this YAT.",
)


api.add_router("items", "todo.api.router", tags=["Items"])

@api.exception_handler(ObjectDoesNotExist)
@api.exception_handler(Http404)
def service_unavailable(request, _):
    return api.create_response(
        request, {"error": "Not Found"}, status=404,
    )
