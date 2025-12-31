from decimal import Decimal
from .models import Portfolio, PortfolioAsset, AssetPrice

def get_initial_quantities():
    # Calcula las cantidades iniciales de todos los activos de los portafolios
    INITIAL_DATE = "2022-02-15"
    # Initial value is set on DB already
    portfolio = Portfolio.objects.all()
    response = []

    for p in portfolio:
        # Get all PortfolioAsset for a portfolio on exact date
        assets = PortfolioAsset.objects.select_related('asset', 'portfolio').filter(portfolio=p, date=INITIAL_DATE)
        portfolio_data = {
            "portfolio" : p.name,
            "initial_value": float(p.initial_value),
            "assets": []
        }

        for a in assets:
            # Get the price on that date on that asset
            asset_price = AssetPrice.objects.get(asset=a.asset, date=INITIAL_DATE)
            price = asset_price.price
            print("PRICE:", price)

            if price > 0 and assets:
                quantity = a.weight * p.initial_value / price

                portfolio_data['assets'].append({
                    "name": a.asset.name,
                    "initial_quantity": float(quantity)

                })
        response.append(portfolio_data)

    return response


def get_values_by_date(start_date, end_date):
    dates = start_date
    for date in dates:
        asset_price = AssetPrice.objects.get(date=date)