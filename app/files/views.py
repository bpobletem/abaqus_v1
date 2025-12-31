from django.views.generic import TemplateView

class PortfolioDashboardView(TemplateView):
    template_name = "app/dashboard.html"