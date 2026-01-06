from django.db import models
from app.files.enums import TransactionType

class Asset(models.Model):
    name = models.CharField(max_length=30, null=False)

class AssetPrice(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    price = models.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        unique_together = ("asset", "date")

class Portfolio(models.Model):
    name = models.TextField(max_length=20, null=False)
    initial_value = models.DecimalField(max_digits=20, decimal_places=10)

class PortfolioAsset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    initial_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        unique_together = ("portfolio", "asset", "initial_date", "end_date")

class Transaction(models.Model):
    type = models.CharField(max_length=7, choices=TransactionType.choices)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=20, decimal_places=10)