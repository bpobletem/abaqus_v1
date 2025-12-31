from decimal import Decimal
from .models import Portfolio, PortfolioAsset, AssetPrice

def get_values_by_date(start_date, end_date):
    dates = start_date - end_date
    # calculamos la cantidad inicial de cada asset
    # calculamos los valores en base a la cantidad * precio corresponidnete
    # para cada date en array dates obtenemos los precios y lo
    for date in dates:
        asset_price = AssetPrice.objects.get(date=date)