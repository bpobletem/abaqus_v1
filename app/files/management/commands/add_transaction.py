from django.core.management.base import BaseCommand
from django.db import transaction
from app.files.services import add_transaction
from app.files.models import Asset
from app.files.enums import TransactionType
from datetime import date

class Command(BaseCommand):
    help = "Ejecuta el rebalanceo del Bonus 2: Venta EEUU y Compra Europa"

    def handle(self, *args, **options):
        portfolio_id = 1
        monto_operacion = 200_000_000
        fecha_operacion = date(2022, 5, 15)
        
        try:
            # Buscamos los activos por nombre
            asset_eeuu = Asset.objects.get(name="EEUU")
            asset_europa = Asset.objects.get(name="Europa")

            with transaction.atomic():
                self.stdout.write(self.style.SUCCESS(f"Iniciando rebalanceo el {fecha_operacion}..."))

                # Operación A: Venta EEUU
                add_transaction(
                    portfolio_id=portfolio_id,
                    asset_id=asset_eeuu.id,
                    type=TransactionType.SELL,
                    amount=monto_operacion,
                    date=fecha_operacion
                )
                self.stdout.write(f" - Venta de $200M en EEUU registrada.")

                # Operación B: Compra Europa
                add_transaction(
                    portfolio_id=portfolio_id,
                    asset_id=asset_europa.id,
                    type=TransactionType.BUY,
                    amount=monto_operacion,
                    date=fecha_operacion
                )
                self.stdout.write(f" - Compra de $200M en Europa registrada.")

            self.stdout.write(self.style.SUCCESS("Rebalanceo completado exitosamente."))

        except Asset.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"Error: Asegúrate de tener los activos creados. {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocurrió un error: {str(e)}"))