from rest_framework.fields import DjangoValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .selector import get_values_by_date


class PortfolioEvolutionApi(APIView):
    class FilterSerializer(serializers.Serializer):
        start_date = serializers.DateField(required=True)
        end_date = serializers.DateField(required=True)

        def validate(self, data):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("La fecha de inicio debe ser anterior a la de fin")
            return data

    def get(self, request):
        serializer = self.FilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        try:
            data = get_values_by_date(
                start_date=serializer.validated_data['start_date'],
                end_date=serializer.validated_data['end_date']
            )
            return Response({"data": data}, status=status.HTTP_200_OK)

        except DjangoValidationError as e:
            return Response({
                "detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({
                "detail": "Ocurrió un error inesperado en el servidor."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )