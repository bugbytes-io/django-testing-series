from django.conf import settings
from django.http import HttpResponse

class MaintenanceModeMiddleware:
    """
    Middleware that checks if the site is in maintenance mode.
    If the MAINTENANCE_MODE setting is True, it returns a "Site under maintenance" response.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'MAINTENANCE_MODE', False):
            return HttpResponse("Site is under maintenance", status=503)
        return self.get_response(request)