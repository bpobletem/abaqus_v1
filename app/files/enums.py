from django.db import models

class TransactionType(models.TextChoices):
    BUY = 'BUY', 'Compra'
    SELL = 'SELL', 'Venta'