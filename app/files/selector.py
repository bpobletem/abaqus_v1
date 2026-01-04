from decimal import Decimal
from .models import Portfolio, PortfolioAsset, AssetPrice

def get_values_by_date(start_date, end_date):
    # Obtenemos todos los precios en el rango de fechas una sola vez
    prices = AssetPrice.objects.filter(date__range=[start_date, end_date]).select_related('asset')

    # Obtenemos las cantidades de los portafolios
    positions = PortfolioAsset.objects.select_related('portfolio', 'asset').all()
    
    # Organizamos los precios en un map para acceso rápido: { (fecha, asset_id): precio }
    price_map = {(p.date, p.asset_id): p.price for p in prices}

    # Obtenemos todas las fechas únicas del rango para iterar
    unique_dates = prices.values_list('date', flat=True).distinct().order_by('date')

    response = []

    for current_date in unique_dates:
        daily_data = {
            "date": current_date,
            "portfolios": []
        }

        # Iteramos por cada portafolio registrado
        for portfolio in Portfolio.objects.all():
            total_value_t = Decimal("0")
            portfolio_assets_data = []

            # Filtramos las posiciones que pertenecen a este portafolio
            portfolio_positions = [
                pos for pos in positions 
                if pos.portfolio_id == portfolio.id 
                and pos.initial_date.date() <= current_date
                and (pos.end_date is None or pos.end_date.date() > current_date)
            ]

            # Calcular el Valor Total del portafolio
            # V_t = Sum(Cantidad_i * Precio_{i,t})
            for pos in portfolio_positions:
                price_t = price_map.get((current_date, pos.asset_id))
                
                if price_t:
                    asset_value_t = pos.quantity * price_t
                    total_value_t += asset_value_t
                    
                    # Guardamos temporalmente para calcular el peso después
                    portfolio_assets_data.append({
                        "asset_name": pos.asset.name,
                        "value_t": asset_value_t
                    })

            # Calcular weight = x_i,t / 
            final_assets = []
            for asset_item in portfolio_assets_data:
                weight_t = asset_item["value_t"] / total_value_t if total_value_t > 0 else 0
                
                final_assets.append({
                    "asset": asset_item["asset_name"],
                    "weight": float(round(weight_t, 8)),
                    "value": float(round(asset_item["value_t"], 2))
                })

            daily_data["portfolios"].append({
                "portfolio_name": portfolio.name,
                "total_value": float(round(total_value_t, 2)),
                "assets": final_assets
            })
            
        response.append(daily_data)

    return response