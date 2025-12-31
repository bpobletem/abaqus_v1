from django.urls import path
from .files.apis import *

urlpatterns = [
    path('health/', HealthCheckApi.as_view(), name='health-check'),
    path('portfolio-evolution/', PortfolioEvolutionApi.as_view(), name='portfolio_evolution'),
]