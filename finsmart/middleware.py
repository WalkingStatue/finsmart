from django.shortcuts import redirect
from django.urls import reverse

class LandingPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Logic for first-time visit
        landing_page_url = reverse('landing_page')
        if not request.session.get('seen_landing_page', False) and not request.user.is_authenticated and request.path != landing_page_url:
            request.session['seen_landing_page'] = True  # Mark the session
            return redirect(landing_page_url)

        response = self.get_response(request)
        return response
