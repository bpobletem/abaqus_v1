from django.conf import settings
from django.db import transaction
from app.files.models import Asset, AssetPrice, Portfolio, PortfolioAsset, Transaction
from decimal import Decimal
from .enums import TransactionType
import pandas as pd

def load_data(file_path: str):
    # Usamos transaction.atomic para que si algo falla, no se cargue nada
    with transaction.atomic():
        # Cargamos el Excel
        weights = pd.read_excel(file_path, sheet_name = 'weights')
        prices_df = pd.read_excel(file_path, sheet_name = 'Precios', decimal=",", parse_dates=["Dates"])

        # Assets
        unique_assets = weights['activos'].unique()
        Asset.objects.bulk_create(
            [Asset(name=name) for name in unique_assets], ignore_conflicts=True
        )

        # AssetPrice
        asset_map = {a.name: a for a in Asset.objects.all()}
        
        prices_long = prices_df.melt(
            id_vars = "Dates",
            var_name = "asset",
            value_name = "price"
        ).dropna(subset = ["price"])

        # Creamos los objetos
        asset_price_objs = [
            AssetPrice(
                asset=asset_map[row["asset"]],
                date=row["Dates"].date(),
                price=Decimal(str(row["price"]))
            )
            for _, row in prices_long.iterrows()
        ]
        AssetPrice.objects.bulk_create(asset_price_objs, ignore_conflicts=True)
        
        # Portfolio 
        # Quitamos las columnas que no son nombres
        INITIAL_CAPITAL = Decimal("1000000000")
        BASE_COLUMNS = {"Fecha", "activos"}
        
        portfolio_names = [
            col for col in weights.columns
            if col not in BASE_COLUMNS
        ]

        # Creamos los objetos y los insertamos
        Portfolio.objects.bulk_create(
            [
                Portfolio(name=col, initial_value=INITIAL_CAPITAL)
                for col in portfolio_names
            ],
            ignore_conflicts=True
        )

        portfolio_map = {p.name: p for p in Portfolio.objects.all()}

        # PortfolioAsset
        initial_date = weights['Fecha'].iloc[0].date()
        asset_prices = AssetPrice.objects.filter(date=initial_date)
        price_map = {(p.asset_id, p.date): Decimal(p.price) for p in asset_prices}
        allocations = []
        
        for _, row in weights.iterrows():
            asset = asset_map[row['activos']]
            price = price_map.get((asset.id, initial_date))
            
            for name in portfolio_map:
                weight = Decimal(str(row[name]))
                quantity = weight * INITIAL_CAPITAL / price

                allocations.append(
                    PortfolioAsset(
                        portfolio=portfolio_map[name],
                        asset=asset,
                        initial_date=initial_date,
                        quantity=quantity
                    )
                )

        PortfolioAsset.objects.bulk_create(allocations)

def add_transaction(*, portfolio_id, asset_id, type, amount, date):
    # Creamos el objecto de Transaction
    transaction_obj = Transaction.objects.create(
        portfolio_id=portfolio_id,
        asset_id=asset_id,
        type=type,
        value=amount,
        date=date
    )

    execute_portfolio_rebalance(
        portfolio_id=portfolio_id,
        asset_id=asset_id,
        type=type,
        amount=amount,
        date=date
    )

    return

def execute_portfolio_rebalance(*, portfolio_id, asset_id, type, amount, date):
    # Obtener precio y cantidad del activo
    price = AssetPrice.objects.get(asset_id=asset_id, date=date).price
    quantity = price / Decimal(amount)
    # Editamos PortfolioAsset actual poniendole end_date
    if type == TransactionType.SELL:
        quantity = -quantity

    # Buscar la posición actual
    current_position = PortfolioAsset.objects.filter(
        portfolio_id=portfolio_id,
        asset_id=asset_id,
        end_date__isnull=True
    ).first()

    if current_position:
        current_position.end_date = date
        current_position.save()
        new_quantity = current_position.quantity + quantity

    # Creamos nuevo PortfolioAsset
    PortfolioAsset.objects.create(
        portfolio_id=portfolio_id,
        asset_id=asset_id,
        initial_date=date,
        quantity=new_quantity
    )
    return