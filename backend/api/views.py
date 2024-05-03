from django.shortcuts import render
from .models import *
from .serializers import *
from .pelosiscraper import RunPelosiScraper
from .financescraper import RunFinanceScraper
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class RunPelosiBot(APIView):
    def post(self, request):
        PelosiTrade.objects.all().delete()
        RunPelosiScraper()
        return Response({"Message": "Scraped data successfully"}, status=status.HTTP_200_OK)
    
class RunStockBot(APIView):
    def post(self, request, stock_id):
        RunFinanceScraper(stock_id)
        return Response({"Message": "Scraped data successfully"}, status=status.HTTP_200_OK)



class GetPelosiTrades(APIView):
    def get(self, request):
        pelosi = PelosiTrade.objects.all()
        if len(pelosi) == 0:
            return Response({"Message": "No Nancy Pelosi stored"}, status=status.HTTP_204_NO_CONTENT)
        serializer = PelosiTradeSerializer(pelosi, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetStocks(APIView):
    def get(self, request):
        stocks = Stock.objects.all()
        if len(stocks) == 0:
            return Response({"Message": "No Stocks stored"}, status=status.HTTP_204_NO_CONTENT)
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetHighestPerformingStock(APIView):
    def get(self, request):
        # Get all stocks
        stocks = Stock.objects.all()

        if not stocks:
            return Response({"Message": "No data stored"}, status=status.HTTP_204_NO_CONTENT)

        # Extract and convert since_transaction values to floats
        performances = []
        for stock in stocks:
            price_str = stock.current_price.replace(',', '')  # Remove commas
            try:
                performance = float(price_str)
                performances.append(performance)
            except ValueError:
                pass  # Ignore if since_transaction cannot be converted to float

        if not performances:
            return Response({"Message": "No valid performance data found"}, status=status.HTTP_204_NO_CONTENT)

        # Find the index of the highest performance
        highest_performance_index = performances.index(max(performances))

        # Get the corresponding stock with the highest performance
        highest_performing_stock = stocks[highest_performance_index]

        # Serialize the highest performing stock data
        serializer = StockSerializer(highest_performing_stock)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetSectorCuts(APIView):
    def post(self, request):
        trades = PelosiTrade.objects.all()
        sector_spending = {}

        # Step 1: Iterate through trades and sum up spending per sector
        for trade in trades:
            if trade.stock_symbol == "-":
                continue
            stock = Stock.objects.filter(stock_symbol=trade.stock_symbol).first()
            if stock:
                sector = stock.sector

                spending_amount = int(''.join(filter(str.isdigit, trade.trade_price)))

                sector_spending[sector] = sector_spending.get(sector, 0) + spending_amount
        
        # Step 2: Calculate total spending
        total_spending = sum(sector_spending.values())

        # Step 3: Calculate percentages spent per sector
        sector_percentages = {sector: (spending / total_spending) * 100 for sector, spending in sector_spending.items()}

        return Response(sector_percentages)

class GetHistoricalData(APIView):
    def get(self, request):
        data = HistoricalData.objects.all()
        if len(data) == 0:
            return Response({"Message": "No data stored"}, status=status.HTTP_204_NO_CONTENT)
        serializer = HistoricalDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetHistoricalDataByStock(APIView):
    def get(self, request, stock_id):
        filtered_data = HistoricalData.objects.filter(stock_symbol=stock_id)
        if len(filtered_data) == 0:
            return Response({"Message": "No data stored"}, status=status.HTTP_204_NO_CONTENT)
        serializer = HistoricalDataSerializer(filtered_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteAPPL(APIView):
    def post(self, request):
        # Delete Stock objects where stock_symbol == 'APPL'
        stocks_to_delete = Stock.objects.filter(stock_symbol='APPL')
        if stocks_to_delete.exists():
            stocks_to_delete.delete()
            return Response("Stocks with stock_symbol 'APPL' deleted successfully.", status=status.HTTP_200_OK)
        else:
            return Response("No stocks found with stock_symbol 'APPL'.", status=status.HTTP_404_NOT_FOUND)

    
class GetNancyPelosi(APIView):
    def get(self, request):
        pelosi = NancyPelosi.objects.first()
        if not pelosi:
            return Response({"Message": "No Nancy Pelosi stored"}, status=status.HTTP_204_NO_CONTENT)
        serializer = NancyPelosiSerializer(pelosi)
        return Response(serializer.data, status=status.HTTP_200_OK)
