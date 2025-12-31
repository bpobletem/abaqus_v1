from django.conf import settings
from django.db import transaction
from app.files.models import Asset, AssetPrice, Portfolio, PortfolioAsset
from decimal import Decimal
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
        asset_prices = AssetPrice.objects.filter(date=initial_date).in_bulk(field_name='asset_id')
        initial_date = weights['Fecha'].iloc[0]
        allocations = []
        
        for _, row in weights.iterrows():
            asset = asset_map[row['activos']]
            price = asset_prices.get(asset.id).price

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