from django.urls import reverse
from django.shortcuts import redirect

class LandingPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        landing_page_url = reverse('landing_page')
        admin_login_url = reverse('admin:login')

        if (
            not request.session.get('seen_landing_page', False)
            and not request.user.is_authenticated
            and request.path != landing_page_url
            and not request.path.startswith('/admin/logout/') 
            and not request.path.startswith('/admin/password_change/')
            and request.path != admin_login_url
        ):
            request.session['seen_landing_page'] = True 
            return redirect(landing_page_url)

        response = self.get_response(request)
        return response