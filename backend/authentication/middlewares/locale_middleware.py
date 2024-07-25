from django.utils import translation
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Callable

class LocaleMiddleware:
    def __init__(self, get_response: Callable[[Request], Response]) -> None:
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:
        language_code = request.session.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
        print(f"Middleware: Current language from session: {language_code}")
        print(f"Session data at middleware: {request.session.items()}")
        translation.activate(language_code)
        response = self.get_response(request)
        return response