from django.utils import translation


# Используется, чтобы во время тестов Хекслета сайт отображался на русском
class SetDefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        translation.activate('ru')
        request.LANGUAGE_CODE = 'ru'
        response = self.get_response(request)
        return response
