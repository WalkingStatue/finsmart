from django.views.generic import TemplateView

class LandingPageView(TemplateView):
    template_name = 'landing_page.html'

    def get_context_data(self, **kwargs):
        # You can add any additional context here if needed
        context = super().get_context_data(**kwargs)
        return context

