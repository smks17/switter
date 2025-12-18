import logging
from django.http.response import JsonResponse


class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if exception is not None:
            logging.error(exception, exc_info=exception)
            return JsonResponse({"error": "Something went wrong."}, status=500)
        return None
