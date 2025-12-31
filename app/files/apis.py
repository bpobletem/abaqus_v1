from django.http import JsonResponse
from django.views import View
from .selector import get_initial_quantities

class HealthCheckApi(View):
    def get(self, request, *args, **kwargs):
        data = {
            "status": 200, 
            "message": "Estructura HackSoftware con Django Vanilla funcionando"
        }
        return JsonResponse(data)

class getInitialQuantities(View):
    def get(self, request, *args, **kwargs):
        try:
            data = get_initial_quantities()
            
            return JsonResponse({
                "status": "success",
                "data": data
            }, status=200)
            
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

class getValues(View):
    def get(self, request, *args, **kwargs):
        # Get fecha_inicio y fecha_fin de los parametros
        # Transformarlo de str a date
        # Obtener valor del activo en las fechas correspondientes
        # Calcular el precio del activo en el tiempo
        # Calcular el weight de cada activo
        # Sumar el precio de los activos para calcular el valor del portafolio
        try: 
            data = {
                "status": 200
            }

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)