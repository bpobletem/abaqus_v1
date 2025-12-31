from django.urls import path
from .files.apis import *

urlpatterns = [
    path('health/', HealthCheckApi.as_view(), name='health-check'),
    path('quantity/', getInitialQuantities.as_view(), name='get-quantities')
]