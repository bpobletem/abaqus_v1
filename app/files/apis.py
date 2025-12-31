from django.http import JsonResponse
from django.views import View
from .selector import get_values_by_date
from datetime import datetime

class HealthCheckApi(View):
    def get(self, request, *args, **kwargs):
        data = {
            "status": 200, 
            "message": "Estructura HackSoftware con Django Vanilla funcionando"
        }
        return JsonResponse(data)

class PortfolioEvolutionApi(View):
    def get(self, request, *args, **kwargs):
        # 1. Capturar parámetros de la URL (?start_date=...&end_date=...)
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # 2. Validación básica de presencia de parámetros
        if not start_date_str or not end_date_str:
            return JsonResponse({
                "status": "error",
                "message": "Debes proporcionar start_date y end_date en formato YYYY-MM-DD"
            }, status=400)

        try:
            # 3. Validar formato de fecha y convertir a objetos date
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date > end_date:
                return JsonResponse({
                    "status": "error", 
                    "message": "start_date no puede ser mayor que end_date"
                }, status=400)

            # 4. Llamar al selector con la lógica de negocio
            data = get_values_by_date(start_date, end_date)

            return JsonResponse({
                "status": "success",
                "data": data
            }, safe=False)

        except ValueError:
            return JsonResponse({
                "status": "error",
                "message": "Formato de fecha inválido. Usa YYYY-MM-DD"
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)