from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .selector import get_values_by_date


class PortfolioEvolutionApi(APIView):
    class FilterSerializer(serializers.Serializer):
        start_date = serializers.DateField(required=True)
        end_date = serializers.DateField(required=True)

    # Validar fechas
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la de fin")
        return data

    def get(self, request):
        # Validar params
        serializer = self.FilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        data = get_values_by_date(**serializer.validated_data)
        
        return Response({"data": data}, status=status.HTTP_200_OK)