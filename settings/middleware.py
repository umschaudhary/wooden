import django

from settings.models import FiscalYear

if django.VERSION >= (1, 10, 0):
    MIDDLEWARE_MIXIN = django.utils.deprecation.MiddlewareMixin
else:
    MIDDLEWARE_MIXIN = object
class SetActiveFiscalYearMiddleware(MIDDLEWARE_MIXIN):
    def process_request(self, request):
        request.active_fiscal_year = FiscalYear.get_active_fiscal_year()

