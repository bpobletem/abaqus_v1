from django.urls import path
from .files.apis import *
from .files.views import *

urlpatterns = [
    path('api/evolution', PortfolioEvolutionApi.as_view(), name='portfolio_evolution'),
    path('dashboard/', PortfolioDashboardView.as_view(), name='dashboard'),
]