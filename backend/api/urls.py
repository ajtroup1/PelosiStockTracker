from django.urls import path
from .views import *

urlpatterns = [
    path('run-pelosi-bot', RunPelosiBot.as_view()),
    path('run-stock-bot/<str:stock_id>', RunStockBot.as_view()),
    path('pelositrades', GetPelosiTrades.as_view()),
    path('nancypelosi', GetNancyPelosi.as_view()),
    path('stocks', GetStocks.as_view()),
    path('highest-stock', GetHighestPerformingStock.as_view()),
    path('get-sector-cuts', GetSectorCuts.as_view()),
    path('historicaldata', GetHistoricalData.as_view()),
    path('historicaldata/<str:stock_id>', GetHistoricalDataByStock.as_view()),
]