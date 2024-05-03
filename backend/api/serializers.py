from rest_framework import serializers
from .models import *

class PelosiTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PelosiTrade
        fields = ['id', 'stock_symbol', 'name', 'trade_type', 'transaction_type', 'trade_date', 'trade_price', 'since_transaction', 'photo_url']

class NancyPelosiSerializer(serializers.ModelSerializer):
    class Meta:
        model = NancyPelosi
        fields = ['net_worth', 'trade_volume', 'total_trades', 'last_traded']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class HistoricalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalData
        fields = '__all__'